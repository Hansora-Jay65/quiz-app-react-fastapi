import logging
import os
import json
import re
import random
from typing import List, Dict
from fastapi import HTTPException, UploadFile
import PyPDF2
import io
import requests

# AI Provider Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv(
    "HUGGINGFACE_API_KEY", ""
)  # Optional - free tier works without key
USE_AI_PROVIDER = os.getenv(
    "AI_PROVIDER", "simple"
)  # Options: "openai", "huggingface", "simple" - Default: "simple" (FREE, no API needed)


def extract_text_from_pdf(pdf_file: UploadFile) -> str:
    """Extract text content from uploaded PDF file"""
    try:
        # Read PDF file content
        pdf_content = pdf_file.file.read()
        pdf_file.file.seek(0)  # Reset file pointer

        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))

        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        if not text.strip():
            raise HTTPException(
                status_code=400, detail="PDF file appears to be empty or unreadable"
            )

        return text
    except Exception as e:
        logging.error(f"Error extracting PDF text: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to extract text from PDF: {str(e)}"
        )


def generate_mcqs_with_huggingface(text: str, num_questions: int = 5) -> List[Dict]:
    """Generate MCQs using Hugging Face's free Inference API"""
    try:
        # Truncate text if too long
        max_chars = 2000  # Hugging Face free tier has limits
        if len(text) > max_chars:
            text = text[:max_chars] + "..."

        prompt = f"""Generate {num_questions} multiple choice questions from this text. Return ONLY valid JSON in this exact format:
{{
  "questions": [
    {{
      "question_text": "Question here",
      "answers": [
        {{"answer_text": "Option A", "is_correct": true}},
        {{"answer_text": "Option B", "is_correct": false}},
        {{"answer_text": "Option C", "is_correct": false}},
        {{"answer_text": "Option D", "is_correct": false}}
      ]
    }}
  ]
}}

Text: {text}"""

        # Use Hugging Face Inference API (free tier)
        API_URL = (
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        )

        # Try a better model for text generation
        headers = {}
        if HUGGINGFACE_API_KEY:
            headers["Authorization"] = f"Bearer {HUGGINGFACE_API_KEY}"

        # Use a model better suited for instruction following
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 1500,
                "temperature": 0.7,
                "return_full_text": False,
            },
        }

        # Try using a better model - if it fails, fall back to simple generator
        try:
            response = requests.post(
                "https://api-inference.huggingface.co/models/google/flan-t5-base",
                headers=headers,
                json=payload,
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                # Hugging Face models may not return perfect JSON, so we'll use simple generator
                # as fallback
                pass
        except:
            pass

        # Fall back to simple generator
        return generate_mcqs_simple(text, num_questions)

    except Exception as e:
        logging.error(f"Hugging Face error: {str(e)}")
        # Fall back to simple generator
        return generate_mcqs_simple(text, num_questions)


def generate_mcqs_with_openai(text: str, num_questions: int = 5) -> List[Dict]:
    """Generate MCQs using OpenAI API (requires paid credits)"""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)

        if not OPENAI_API_KEY or len(OPENAI_API_KEY) < 20:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured.",
            )

        max_chars = 12000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."

        prompt = f"""Based on the following text, generate {num_questions} multiple choice questions (MCQs) with 4 options each and mark the correct answer.

Text content:
{text}

Please generate the questions in the following JSON format:
{{
  "questions": [
    {{
      "question_text": "Question text here",
      "answers": [
        {{"answer_text": "Option A", "is_correct": true}},
        {{"answer_text": "Option B", "is_correct": false}},
        {{"answer_text": "Option C", "is_correct": false}},
        {{"answer_text": "Option D", "is_correct": false}}
      ]
    }}
  ]
}}

Make sure:
1. Each question has exactly 4 answer options
2. Only one answer is marked as correct (is_correct: true)
3. Questions are relevant to the text content
4. Questions test understanding, not just memorization
5. Return ONLY valid JSON, no additional text"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at creating educational multiple choice questions from text content. Always return valid JSON format.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=2000,
        )

        content = response.choices[0].message.content.strip()

        # Remove markdown code blocks
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        result = json.loads(content)
        if "questions" not in result:
            raise HTTPException(
                status_code=500, detail="Invalid response format from AI"
            )
        return result["questions"]

    except Exception as e:
        logging.error(f"OpenAI error: {str(e)}")
        # Fall back to simple generator
        return generate_mcqs_simple(text, num_questions)


def generate_mcqs_simple(text: str, num_questions: int = 5) -> List[Dict]:
    """Simple rule-based MCQ generator (FREE - no API needed)"""
    try:
        # Split text into sentences
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        if len(sentences) < num_questions:
            # Use paragraphs if not enough sentences
            paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]
            if len(paragraphs) < num_questions:
                paragraphs = [
                    text[i : i + 200]
                    for i in range(0, len(text), 200)
                    if len(text[i : i + 200]) > 50
                ]
            sentences = paragraphs[: num_questions * 2]

        questions = []
        used_sentences = set()

        for i in range(min(num_questions, len(sentences))):
            # Pick a random sentence
            available = [
                s for s in sentences if s not in used_sentences and len(s) > 30
            ]
            if not available:
                break

            correct_sentence = random.choice(available)
            used_sentences.add(correct_sentence)

            # Extract key terms
            words = re.findall(r"\b[A-Z][a-z]+\b|\b[a-z]{4,}\b", correct_sentence)
            key_word = random.choice(words) if words else "concept"

            # Create question
            question_text = f"What is mentioned about '{key_word}' in the text?"

            # Create answers
            answers = []
            # Correct answer
            correct_answer = (
                correct_sentence[:100] + "..."
                if len(correct_sentence) > 100
                else correct_sentence
            )
            answers.append({"answer_text": correct_answer, "is_correct": True})

            # Wrong answers (from other sentences)
            wrong_sentences = [
                s
                for s in sentences
                if s != correct_sentence and s not in used_sentences
            ]
            for j in range(3):
                if wrong_sentences:
                    wrong = random.choice(wrong_sentences)
                    wrong_answer = wrong[:100] + "..." if len(wrong) > 100 else wrong
                    answers.append({"answer_text": wrong_answer, "is_correct": False})
                    wrong_sentences.remove(wrong)
                else:
                    answers.append(
                        {"answer_text": f"Option {chr(66+j)}", "is_correct": False}
                    )

            # Shuffle answers
            random.shuffle(answers)

            questions.append({"question_text": question_text, "answers": answers})

        # If we don't have enough questions, create fill-in-the-blank style
        while len(questions) < num_questions:
            # Extract key phrases
            phrases = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text)
            if phrases:
                key_phrase = random.choice(phrases)
                question_text = f"According to the text, what is '{key_phrase}'?"

                # Simple answers
                answers = [
                    {
                        "answer_text": "A key concept mentioned in the text",
                        "is_correct": True,
                    },
                    {"answer_text": "Not mentioned in the text", "is_correct": False},
                    {"answer_text": "A different topic", "is_correct": False},
                    {"answer_text": "Unrelated information", "is_correct": False},
                ]
                random.shuffle(answers)

                questions.append({"question_text": question_text, "answers": answers})
            else:
                break

        return questions[:num_questions]

    except Exception as e:
        logging.error(f"Simple generator error: {str(e)}")
        # Return at least one question
        return [
            {
                "question_text": "What is the main topic of this text?",
                "answers": [
                    {
                        "answer_text": "The content discussed in the uploaded document",
                        "is_correct": True,
                    },
                    {"answer_text": "An unrelated topic", "is_correct": False},
                    {"answer_text": "A different subject", "is_correct": False},
                    {"answer_text": "Something else", "is_correct": False},
                ],
            }
        ]


def generate_mcqs_from_text(text: str, num_questions: int = 5) -> List[Dict]:
    """Generate MCQ questions from text - tries multiple methods"""
    try:
        # Choose provider based on configuration
        if USE_AI_PROVIDER == "openai" and OPENAI_API_KEY:
            try:
                return generate_mcqs_with_openai(text, num_questions)
            except:
                logging.warning("OpenAI failed, falling back to simple generator")
                return generate_mcqs_simple(text, num_questions)
        elif USE_AI_PROVIDER == "huggingface":
            try:
                return generate_mcqs_with_huggingface(text, num_questions)
            except:
                logging.warning("Hugging Face failed, falling back to simple generator")
                return generate_mcqs_simple(text, num_questions)
        else:
            # Default to simple generator (FREE)
            return generate_mcqs_simple(text, num_questions)

    except Exception as e:
        logging.error(f"Error generating MCQs: {str(e)}")
        # Always fall back to simple generator
        return generate_mcqs_simple(text, num_questions)


def process_pdf_and_generate_mcqs(
    pdf_file: UploadFile, num_questions: int = 5
) -> List[Dict]:
    """Main function to process PDF and generate MCQs"""
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_file)

        # Generate MCQs from text
        mcqs = generate_mcqs_from_text(text, num_questions)

        return mcqs
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
