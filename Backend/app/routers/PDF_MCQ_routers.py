from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from ..services.PDF_MCQ_Services import process_pdf_and_generate_mcqs
from ..services.Quiz_Services import create_quiz
from ..services.Question_Services import create_question
from ..services.Answer_Services import create_answer
from ..models.Quiz_Model import QuizBase
from ..models.Question_Model import QuestionBase
from ..models.Answer_Model import AnswerBase
from ..utils.validation import (
    validate_pdf_file,
    validate_num_questions,
    sanitize_quiz_title,
    sanitize_creator_name,
)
from datetime import datetime
import logging
import json
from ..rate_limiter import limiter

router = APIRouter(prefix="/PDF_MCQ", tags=["PDF MCQ Generator"])


@router.post("/generate-mcqs")
@limiter.limit("5/hour")  # 5 PDF processing per hour per IP (resource-intensive)
async def generate_mcqs_from_pdf(
    request: Request,
    file: UploadFile = File(...),
    num_questions: int = Form(5),
    quiz_title: str = Form(None),
    created_by: str = Form(None),
):
    """
    Upload a PDF file and generate MCQs from it.
    Optionally create a quiz with the generated questions.
    """
    try:
        # Read file content for validation
        file_content = await file.read()
        await file.seek(0)  # Reset file pointer

        # Validate PDF file (type, size, magic bytes)
        validate_pdf_file(file_content, file.filename)

        # Validate number of questions
        num_questions = validate_num_questions(num_questions)

        # Sanitize quiz title and creator name if provided
        if quiz_title:
            quiz_title = sanitize_quiz_title(quiz_title)
        if created_by:
            created_by = sanitize_creator_name(created_by)

        # Process PDF and generate MCQs
        mcqs = process_pdf_and_generate_mcqs(file, num_questions)

        result = {
            "message": "MCQs generated successfully",
            "num_questions": len(mcqs),
            "questions": mcqs,
        }

        # If quiz_title and created_by are provided, create quiz and questions
        if quiz_title and created_by:
            try:
                # Create quiz
                quiz_data = QuizBase(
                    quiz_title=quiz_title,
                    created_by=created_by,
                    created_at=datetime.now(),
                )
                quiz_result = create_quiz(quiz_data)
                quiz_id = quiz_result.quiz_id

                # Create questions and answers
                created_questions = []
                for mcq in mcqs:
                    # Create question
                    question_data = QuestionBase(
                        quiz_id=quiz_id, question_text=mcq["question_text"]
                    )
                    question_result = create_question(question_data)
                    # Extract question_id from JSONResponse
                    response_data = json.loads(question_result.body.decode())
                    question_id = response_data.get("Question", {}).get("question_id")

                    if not question_id:
                        raise HTTPException(
                            status_code=500,
                            detail="Failed to get question_id from response",
                        )

                    # Create answers
                    for answer in mcq["answers"]:
                        answer_data = AnswerBase(
                            question_id=question_id,
                            answer_text=answer["answer_text"],
                            is_correct=answer["is_correct"],
                        )
                        create_answer(answer_data)

                    created_questions.append(
                        {
                            "question_id": question_id,
                            "question_text": mcq["question_text"],
                        }
                    )

                result["quiz_created"] = True
                result["quiz_id"] = quiz_id
                result["created_questions"] = created_questions

            except Exception as e:
                logging.error(f"Error creating quiz: {str(e)}")
                result["quiz_created"] = False
                result["error"] = f"MCQs generated but quiz creation failed: {str(e)}"

        return result

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in generate_mcqs_from_pdf: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to process request: {str(e)}"
        )


@router.post("/generate-mcqs-only")
@limiter.limit("5/hour")  # 5 PDF processing per hour per IP
async def generate_mcqs_only(
    request: Request, file: UploadFile = File(...), num_questions: int = Form(5)
):
    """
    Upload a PDF file and generate MCQs without creating a quiz.
    Returns only the generated questions.
    """
    try:
        # Read file content for validation
        file_content = await file.read()
        await file.seek(0)  # Reset file pointer

        # Validate PDF file (type, size, magic bytes)
        validate_pdf_file(file_content, file.filename)

        # Validate number of questions
        num_questions = validate_num_questions(num_questions)

        mcqs = process_pdf_and_generate_mcqs(file, num_questions)

        return {
            "message": "MCQs generated successfully",
            "num_questions": len(mcqs),
            "questions": mcqs,
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in generate_mcqs_only: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to process request: {str(e)}"
        )
