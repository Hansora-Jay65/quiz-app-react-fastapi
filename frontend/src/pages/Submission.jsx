import React, { useEffect, useState } from "react";
import { useLocation, useParams, useNavigate } from "react-router-dom";
import { getQuizStatistics } from "../services/api";
import "../styles/ResultPage.css";

function ResultPage() {
  const navigate = useNavigate();
  const { quizId } = useParams();
  const location = useLocation();
  const { correct, wrong, total } = location.state || {};

  const [stats, setStats] = useState(null);
  const [statsError, setStatsError] = useState("");

  useEffect(() => {
    if (!quizId) return;

    getQuizStatistics(quizId)
      .then((res) => {
        setStats(res.data);
        setStatsError("");
      })
      .catch((err) => {
        console.error("Failed to load quiz statistics", err.response?.data || err.message);
        setStats(null);
        setStatsError("Stats are not available yet for this quiz.");
      });
  }, [quizId]);

  const goToLeaderboard = () => {
    navigate("/leaderboard"); 
  };

  if (!location.state) {
    return (
      <div className="result-container">
        <p className="error-text">⚠️ No result data found. Please take the quiz first.</p>
      </div>
    );
  }

  return (
    <div className="result-container">
      <h2 className="result-title">🎉 Quiz {quizId} Result</h2>

      <div className="result-stats">
        <p className="correct">✅ Correct Answers: {correct}</p>
        <p className="wrong">❌ Wrong Answers: {wrong}</p>
        <p className="total">📊 Total Questions: {total}</p>
      </div>

      <h3 className="final-score">
        Your Score: <span>{correct} / {total}</span>
      </h3>

      {stats && (
        <div className="quiz-stats">
          <h4>📈 Quiz Statistics</h4>
          <p>
            Average Score: <strong>{stats.average_score?.toFixed(2)}</strong>
            {stats.total_questions > 0 && stats.average_percentage !== null && (
              <> ({stats.average_percentage}% of {stats.total_questions} questions)</>
            )}
          </p>
          <p>
            Best Score: <strong>{stats.best_score}</strong>
            {stats.total_questions > 0 && stats.best_percentage !== null && (
              <> ({stats.best_percentage}% of {stats.total_questions} questions)</>
            )}
          </p>
          <p>Total Attempts on this Quiz: <strong>{stats.total_attempts}</strong></p>
        </div>
      )}

      {!stats && statsError && (
        <p className="stats-message">{statsError}</p>
      )}

      <button className="btn-dashboard" onClick={goToLeaderboard}>
        Go to Leaderboard
      </button>
    </div>
  );
}

export default ResultPage;
