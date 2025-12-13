import React, { useEffect, useState } from "react";
import { useAuth } from "../components/AuthContext";
import { getSubmissionsByUser, getAllQuizzes, getQuizStatistics } from "../services/api";
import "../styles/analytics.css";

function AnalyticsDashboard() {
  const { user } = useAuth();
  const [submissions, setSubmissions] = useState([]);
  const [quizzes, setQuizzes] = useState([]);
  const [selectedQuizId, setSelectedQuizId] = useState(null);
  const [quizStats, setQuizStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [statsError, setStatsError] = useState("");

  useEffect(() => {
    if (!user?.id) {
      setLoading(false);
      return;
    }

    Promise.all([
      getSubmissionsByUser(user.id),
      getAllQuizzes(),
    ])
      .then(([subRes, quizRes]) => {
        setSubmissions(subRes.data || []);
        setQuizzes(quizRes.data || []);
      })
      .catch((err) => {
        console.error("Failed to load analytics data", err.response?.data || err.message);
      })
      .finally(() => setLoading(false));
  }, [user]);

  useEffect(() => {
    if (!selectedQuizId) {
      setQuizStats(null);
      setStatsError("");
      return;
    }

    getQuizStatistics(selectedQuizId)
      .then((res) => {
        setQuizStats(res.data);
        setStatsError("");
      })
      .catch((err) => {
        console.error("Failed to load quiz stats", err.response?.data || err.message);
        setQuizStats(null);
        setStatsError("No stats available for this quiz yet.");
      });
  }, [selectedQuizId]);

  if (!user) {
    return (
      <div className="analytics-page">
        <div className="analytics-card">
          <h2>📊 Quiz Analytics</h2>
          <p>Please log in to see your quiz analytics.</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="analytics-page">
        <div className="analytics-card">
          <p>Loading analytics...</p>
        </div>
      </div>
    );
  }

  const userEmail = user.email;

  return (
    <div className="analytics-page">
      <div className="analytics-card">
        <h2>📊 Quiz Analytics Dashboard</h2>
        <p className="analytics-user">Signed in as: <strong>{userEmail}</strong></p>

        <section className="analytics-section">
          <h3>Your Quiz History</h3>
          {submissions.length === 0 ? (
            <p>You have not submitted any quizzes yet.</p>
          ) : (
            <table className="analytics-table">
              <thead>
                <tr>
                  <th>Submission ID</th>
                  <th>Quiz ID</th>
                  <th>Score</th>
                  <th>Submitted At</th>
                </tr>
              </thead>
              <tbody>
                {submissions.map((s) => (
                  <tr key={s.submission_id}>
                    <td>{s.submission_id}</td>
                    <td>{s.quiz_id}</td>
                    <td>{s.score}</td>
                    <td>{s.submitted_at}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>

        <section className="analytics-section">
          <h3>Quiz Overview</h3>
          <div className="quiz-selector">
            <label>Select a quiz to see stats:</label>
            <select
              value={selectedQuizId || ""}
              onChange={(e) => setSelectedQuizId(e.target.value ? Number(e.target.value) : null)}
            >
              <option value="">-- Select quiz --</option>
              {quizzes.map((q) => (
                <option key={q.quiz_id} value={q.quiz_id}>
                  {q.quiz_title} (ID: {q.quiz_id})
                </option>
              ))}
            </select>
          </div>

          {quizStats && (
            <div className="quiz-stats-panel">
              <h4>Stats for Quiz ID {quizStats.quiz_id}</h4>
              <p>Total Attempts: <strong>{quizStats.total_attempts}</strong></p>
              <p>
                Average Score: <strong>{quizStats.average_score?.toFixed(2)}</strong>
                {quizStats.total_questions > 0 && quizStats.average_percentage !== null && (
                  <> ({quizStats.average_percentage}% of {quizStats.total_questions} questions)</>
                )}
              </p>
              <p>
                Best Score: <strong>{quizStats.best_score}</strong>
                {quizStats.total_questions > 0 && quizStats.best_percentage !== null && (
                  <> ({quizStats.best_percentage}% of {quizStats.total_questions} questions)</>
                )}
              </p>
            </div>
          )}

          {!quizStats && statsError && (
            <p className="analytics-message">{statsError}</p>
          )}
        </section>
      </div>
    </div>
  );
}

export default AnalyticsDashboard;
