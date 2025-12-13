import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/quizDashboard.css";

function QuizHomePage() {
  const navigate = useNavigate();

  return (
    <div className="dashboard-page">
      <div className="dashboard-card">
        <h1>Welcome to Quiz App 🎉</h1>
        <p>Select an action below to manage or play quizzes.</p>

        <div className="button-grid">
          <button className="btn" onClick={() => navigate("/quizList")}>
            📋 View Quizzes
          </button>
          <button className="btn" onClick={() => navigate("/createQuizPage")}>
            ➕ Create Quiz
          </button>
          <button className="btn" onClick={() => navigate("/updateQuizQuestionAnswer")}>
            ✏️ Update Quiz
          </button>
          <button className="btn" onClick={() => navigate("/deleteQuiz")}>
            ❌ Delete Quiz
          </button>
          <button className="btn primary" onClick={() => navigate("/leaderboard")}>
            🏆 Leaderboard
          </button>
        </div>
      </div>
    </div>
  );
}

export default QuizHomePage;
