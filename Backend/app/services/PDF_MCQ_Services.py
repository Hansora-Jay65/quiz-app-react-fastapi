import logging
import os
import json
import re
import random
from typing import List, Dict
from fastapi import HTTPException, UploadFile
import PyPDF2
import io

# Groq LangChain imports
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# AI Provider Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
USE_AI_PROVIDER = os.getenv("AI_PROVIDER")  # Options: "groq", "simple" - Default: "groq"

# Initialize Groq client if key is present
_groq_llm = None
if GROQ_API_KEY:
    try:
        _groq_llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            top_p=0.9
        )
        logging.info("Groq LLM initialized successfully")
    except Exception as e:
        logging.error(f"Failed to initialize Groq LLM: {e}")
        _groq_llm = None
else:
    logging.warning("Groq API key not provided")


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


def generate_mcqs_with_groq(text: str, num_questions: int = 5) -> List[Dict]:
    """Generate MCQs using Groq AI (Llama 3.3 70B)."""
    if not _groq_llm:
        logging.warning("Groq LLM not initialized, falling back to simple generator")
        return generate_mcqs_simple(text, num_questions)

    try:
        max_chars = 12000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."

        # Create prompt template for Groq
        mcq_prompt = PromptTemplate(
            input_variables=["context", "num_questions"],
            template="""
You are an expert educator creating diverse multiple-choice questions. Generate {num_questions} UNIQUE questions about the text below.

IMPORTANT: 
- Each question must be DIFFERENT and cover different aspects
- Vary question types (what, how, why, which, etc.)
- Cover different topics from the text
- Avoid repetition

Text:
{context}

Generate {num_questions} distinct MCQs:

## MCQ 1
Question: [unique question 1]
A) [option A]
B) [option B]
C) [option C]
D) [option D]
Correct Answer: [correct option]

## MCQ 2
Question: [unique question 2]
A) [option A]
B) [option B]
C) [option C]
D) [option D]
Correct Answer: [correct option]

## MCQ 3
Question: [unique question 3]
A) [option A]
B) [option B]
C) [option C]
D) [option D]
Correct Answer: [correct option]

## MCQ 4
Question: [unique question 4]
A) [option A]
B) [option B]
C) [option C]
D) [option D]
Correct Answer: [correct option]

## MCQ 5
Question: [unique question 5]
A) [option A]
B) [option B]
C) [option C]
D) [option D]
Correct Answer: [correct option]
"""
        )

        # Create chain
        mcq_chain = mcq_prompt | _groq_llm | StrOutputParser()

        # Generate MCQs
        response = mcq_chain.invoke({
            "context": text,
            "num_questions": num_questions
        }).strip()

        logging.info(f"Groq raw output:\n{response}")

        # Parse the response
        questions = parse_groq_output(response)

        if not questions:
            logging.warning("Groq parsing produced no questions, falling back to simple generator")
            return generate_mcqs_simple(text, num_questions)

        return questions

    except Exception as e:
        logging.error(f"Groq error: {str(e)}")
        return generate_mcqs_simple(text, num_questions)


def generate_mcqs_simple(text: str, num_questions: int = 5) -> List[Dict]:
    """Simple rule-based MCQ generator (FREE - no API needed)"""
    try:
        # Split text into sentences
        print(text)
        sentences = re.split(r"[.!?]+", text)
        print(sentences)
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
    """Generate MCQ questions from text - tries Groq first, then simple fallback"""
    try:
        logging.info(f"AI provider: {USE_AI_PROVIDER}, Groq available: {_groq_llm is not None}")

        # Choose provider based on configuration
        if USE_AI_PROVIDER == "groq" and _groq_llm:
            try:
                return generate_mcqs_with_groq(text, num_questions)
            except:
                logging.warning("Groq failed, falling back to simple generator")
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


def parse_groq_output(text: str):
    """Parse Groq output format into MCQ list."""
    questions = []

    # Split on ## MCQ pattern
    blocks = re.split(r'##\s*MCQ\s*\d+', text.strip())

    for block in blocks:
        if not block.strip():
            continue

        lines = [ln.strip() for ln in block.split('\n') if ln.strip()]
        if len(lines) < 6:
            continue

        # Find question line
        question_text = ""
        options = {}
        correct_answer = ""

        for line in lines:
            if line.startswith("Question:"):
                question_text = line.replace("Question:", "").strip()
            elif re.match(r'^[ABCD]\)', line):
                label = line[0]
                option_text = line[3:].strip()
                options[label] = option_text
            elif line.startswith("Correct Answer:"):
                # Extract the letter from "Correct Answer: B) ..." or "Correct Answer: B"
                correct_match = re.search(r'Correct Answer:\s*([ABCD])', line)
                if correct_match:
                    correct_answer = correct_match.group(1)
                else:
                    # Try to extract from "B) ..." format
                    correct_match = re.search(r'Correct Answer:\s*([ABCD])\)', line)
                    if correct_match:
                        correct_answer = correct_match.group(1)

        # Validate we have all components
        if question_text and len(options) == 4 and correct_answer:
            answers = []
            for label in ['A', 'B', 'C', 'D']:
                answers.append({
                    "answer_text": options[label],
                    "is_correct": (label == correct_answer)
                })

            questions.append({
                "question_text": question_text,
                "answers": answers
            })

    return questions
