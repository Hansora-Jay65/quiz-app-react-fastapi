import React, { useEffect, useState } from "react";
import {
  getAllQuizzes,
  getQustionsByQuiz,
  updateQuestion,
  updateAnswer,
} from "../services/api";
import { useToast } from "../components/ToastContext";
import "../styles/updateQuizQuestion.css";

function UpdateQuizQuestion() {
  const [quizzes, setQuizzes] = useState([]);
  const [selectedQuizId, setSelectedQuizId] = useState("");
  const [questions, setQuestions] = useState([]);
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [updatedQuestionText, setUpdatedQuestionText] = useState("");
  const { showToast } = useToast();

  useEffect(() => {
    getAllQuizzes()
      .then((res) => setQuizzes(res.data))
      .catch(console.error);
  }, []);

  useEffect(() => {
    if (selectedQuizId) {
      getQustionsByQuiz(selectedQuizId)
        .then((res) => setQuestions(res.data))
        .catch(console.error);
    }
  }, [selectedQuizId]);

  const handleSelectQuestion = (q) => {
    setSelectedQuestion(q);
    setUpdatedQuestionText(q.question_text);
  };

  const handleUpdateQuestion = async () => {
    if (!selectedQuestion) return;

    const confirmUpdate = window.confirm("Are you sure you want to update this question?");
    if (!confirmUpdate) return;

    try {
      await updateQuestion(
        selectedQuizId,
        updatedQuestionText,
        selectedQuestion.question_id
      );

      // ✅ Update all answers
      for (let ans of selectedQuestion.answers) {
        await updateAnswer(
          selectedQuestion.question_id,
          ans.answer_id,
          ans.answer_text,
          ans.is_true
        );
      }

      showToast({
        type: "success",
        message: "Question & answers updated successfully.",
      });
    } catch (err) {
      console.error(err);
      showToast({
        type: "error",
        message: "Failed to update question/answers. Please try again.",
      });
    }
  };

  const handleAnswerChange = (answerId, field, value) => {
    setSelectedQuestion((prev) => ({
      ...prev,
      answers: prev.answers.map((ans) =>
        ans.answer_id === answerId ? { ...ans, [field]: value } : ans
      ),
    }));
  };

  const handleCorrectAnswer = (answerId) => {
    setSelectedQuestion((prev) => ({
      ...prev,
      answers: prev.answers.map((ans) => ({
        ...ans,
        is_true: ans.answer_id === answerId,
      })),
    }));
  };

  return (
    <div className="update-container">
      <div className="update-card">
        <h1>✏️ Update Quiz Question</h1>

        <label>Select Quiz:</label>
        <select
          onChange={(e) => setSelectedQuizId(e.target.value)}
          value={selectedQuizId}
        >
          <option value="">-- Select Quiz --</option>
          {quizzes.map((quiz) => (
            <option key={quiz.quiz_id} value={quiz.quiz_id}>
              {quiz.quiz_title}
            </option>
          ))}
        </select>

        {questions.length > 0 && (
          <>
            <label>Select Question:</label>
            <select
              onChange={(e) =>
                handleSelectQuestion(
                  questions.find((q) => q.question_id == e.target.value)
                )
              }
            >
              <option value="">-- Select Question --</option>
              {questions.map((q) => (
                <option key={q.question_id} value={q.question_id}>
                  {q.question_text}
                </option>
              ))}
            </select>
          </>
        )}

        {selectedQuestion && (
          <div className="update-form">
            <label>Question Text:</label>
            <input
              type="text"
              value={updatedQuestionText}
              onChange={(e) => setUpdatedQuestionText(e.target.value)}
            />

            <h3>Update Answers</h3>
            {selectedQuestion.answers.map((ans) => (
              <div key={ans.answer_id} className="answer-row">
                <input
                  type="text"
                  value={ans.answer_text}
                  onChange={(e) =>
                    handleAnswerChange(ans.answer_id, "answer_text", e.target.value)
                  }
                />
                <label className="radio-label">
                  <input
                    type="radio"
                    name="correct"
                    checked={ans.is_true}
                    onChange={() => handleCorrectAnswer(ans.answer_id)}
                  />
                  Correct
                </label>
              </div>
            ))}

            <button className="update-btn" onClick={handleUpdateQuestion}>
              ✅ Update Question
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default UpdateQuizQuestion;
