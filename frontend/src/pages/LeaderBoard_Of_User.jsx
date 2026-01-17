import React, { useEffect, useState } from "react";
import { getSubmissionsByUser, getAllQuizzes } from "../services/api";
import "../styles/Leaderboard.css";

function Leaderboard() {
  const [submissions, setSubmissions] = useState([]);
  const [quizzes, setQuizzes] = useState([]);

  const userId = localStorage.getItem("user_id");
  const userEmail = localStorage.getItem("user_email");

  useEffect(() => {
    getAllQuizzes()
      .then((res) => setQuizzes(res.data))
      .catch(console.error);

    if (userId) {
      getSubmissionsByUser(userId)
        .then((res) => setSubmissions(res.data))
        .catch(console.error);
    }
  }, [userId]);

  const getQuizTitle = (quizId) => {
    const quiz = quizzes.find((q) => q.quiz_id === quizId);
    return quiz ? quiz.quiz_title : `Quiz #${quizId}`;
  };

  return (
    <div className="leaderboard-container">
      <h1 className="leaderboard-title">📊 Leaderboard</h1>
      <p className="user-email">
        <b>User:</b> {userEmail}
      </p>

      {submissions.length === 0 ? (
        <p className="no-data">⚠️ No quizzes attempted yet.</p>
      ) : (
        <table className="leaderboard-table">
          <thead>
            <tr>
              <th>Quiz</th>
              <th>Score</th>
              <th>Submitted At</th>
            </tr>
          </thead>
          <tbody>
            {submissions.map((s) => (
              <tr key={s.submission_id}>
                <td>{getQuizTitle(s.quiz_id)}</td>
                <td>{s.score}</td>
                <td>{new Date(s.submitted_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Leaderboard;
