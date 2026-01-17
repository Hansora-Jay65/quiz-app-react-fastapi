import React, { useEffect, useState } from "react";
import { getQustionsByQuiz, createSubmission } from "../services/api";
import { useParams, useNavigate } from "react-router-dom";
import "../styles/question.css";

function Question() {
  const { quizId } = useParams();
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes per quiz by default
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    getQustionsByQuiz(quizId)
      .then((res) => {
        setQuestions(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [quizId]);

  // Countdown timer effect
  useEffect(() => {
    if (loading || questions.length === 0 || isSubmitting) return;

    if (timeLeft <= 0) {
      // Auto-submit when time is up
      handleSubmit();
      return;
    }

    const timerId = setInterval(() => {
      setTimeLeft((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);

    return () => clearInterval(timerId);
  }, [loading, questions.length, timeLeft, isSubmitting]);

  const handleSelect = (questionId, answerId) => {
    setUserAnswers((prev) => ({
      ...prev,
      [questionId]: answerId,
    }));
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    }
  };

  const handleSubmit = async () => {
    if (isSubmitting) return;
    setIsSubmitting(true);
    let correct = 0,
      wrong = 0;

    questions.forEach((q) => {
      const chosen = userAnswers[q.question_id];
      const correctAns = q.answers.find((a) => a.is_correct);
      if (chosen === correctAns?.answer_id) {
        correct++;
      } else {
        wrong++;
      }
    });

    const userId = localStorage.getItem("user_id");

    const resultData = {
      user_id: parseInt(userId),
      quiz_id: parseInt(quizId),
      score: correct,
      submitted_at: new Date().toISOString(),
    };

    try {
      await createSubmission(resultData);
      navigate(`/result/${quizId}`, {
        state: { correct, wrong, total: questions.length },
      });
    } catch (err) {
      console.error("Error creating submission:", err);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="question-container loading-state">
        <div className="question-card skeleton">
          <div className="skeleton-header" />
          <div className="skeleton-line" />
          <div className="skeleton-line short" />
          <ul className="skeleton-answers">
            <li className="skeleton-pill" />
            <li className="skeleton-pill" />
            <li className="skeleton-pill" />
            <li className="skeleton-pill" />
          </ul>
          <div className="loading-footer">
            <span className="spinner" />
            <span>Loading questions...</span>
          </div>
        </div>
      </div>
    );
  }

  if (questions.length === 0) {
    return <div className="loading">⚠️ No questions available.</div>;
  }

  const currentQuestion = questions[currentIndex];
  const progressPercent = ((currentIndex + 1) / questions.length) * 100;

  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;

  return (
    <div className="question-container">
      <div className="question-card">
        {/* Progress bar */}
        <div className="progress-bar">
          <div className="progress" style={{ width: `${progressPercent}%` }}></div>
        </div>

        <div className="timer-row">
          <span className="timer-label">⏱️ Time Left:</span>
          <span className={`timer-value ${timeLeft <= 30 ? "low" : ""}`}>
            {minutes.toString().padStart(2, "0")}:
            {seconds.toString().padStart(2, "0")}
          </span>
        </div>

        <h2>
          Question {currentIndex + 1} of {questions.length}
        </h2>
        <p className="question-text">{currentQuestion.question_text}</p>

        <ul className="answer-list">
          {currentQuestion.answers.map((ans) => (
            <li
              key={ans.answer_id}
              className={`answer-option ${
                userAnswers[currentQuestion.question_id] === ans.answer_id
                  ? "selected"
                  : ""
              }`}
              onClick={() =>
                handleSelect(currentQuestion.question_id, ans.answer_id)
              }
            >
              <input
                type="radio"
                name={`q-${currentQuestion.question_id}`}
                checked={
                  userAnswers[currentQuestion.question_id] === ans.answer_id
                }
                onChange={() =>
                  handleSelect(currentQuestion.question_id, ans.answer_id)
                }
              />
              <label>{ans.answer_text}</label>
            </li>
          ))}
        </ul>

        <div className="button-group">
          {currentIndex < questions.length - 1 && (
            <button className="btn next-btn" onClick={handleNext}>
              Next ➡️
            </button>
          )}
          {currentIndex === questions.length - 1 && (
            <button className="btn submit-btn" onClick={handleSubmit}>
              ✅ Submit
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default Question;
