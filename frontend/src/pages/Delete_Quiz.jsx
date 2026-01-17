import React, { useEffect, useState } from "react";
import { deleteQuiz, getAllQuizzes } from "../services/api";
import { useToast } from "../components/ToastContext";
import "../styles/deleteQuiz.css";

function DeleteQuiz() {
  const [quizzes, setQuizzes] = useState([]);
  const [selectedQuizId, setSelectedQuizId] = useState("");
  const { showToast } = useToast();

  useEffect(() => {
    getAllQuizzes()
      .then((res) => setQuizzes(res.data))
      .catch(console.error);
  }, []);

  const handleDeleteQuiz = async (quiz_id) => {
    if (!quiz_id) {
      showToast({
        type: "warning",
        message: "Please select a quiz to delete.",
      });
      return;
    }

    const confirmDelete = window.confirm("Are you sure you want to delete this quiz?");
    if (!confirmDelete) return;

    try {
      await deleteQuiz(quiz_id);
      showToast({
        type: "success",
        message: "Quiz deleted successfully.",
      });

      // Remove from state without refresh
      setQuizzes((prev) => prev.filter((q) => q.quiz_id !== parseInt(quiz_id)));
      setSelectedQuizId("");
    } catch (err) {
      console.error(err);
      showToast({
        type: "error",
        message: "Failed to delete quiz. Please try again.",
      });
    }
  };

  return (
    <div className="delete-quiz-container">
      <div className="delete-quiz-card">
        <h1>🗑️ Delete Quiz</h1>

        <label>Select a Quiz:</label>
        <select
          onChange={(e) => setSelectedQuizId(e.target.value)}
          value={selectedQuizId}
        >
          <option disabled value="">
            -- Choose a quiz --
          </option>
          {quizzes.map((quiz) => (
            <option key={quiz.quiz_id} value={quiz.quiz_id}>
              {quiz.quiz_title}
            </option>
          ))}
        </select>

        <button
          onClick={() => handleDeleteQuiz(selectedQuizId)}
          className="delete-btn"
        >
          Delete Quiz
        </button>
      </div>
    </div>
  );
}

export default DeleteQuiz;
