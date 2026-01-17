import React, { useEffect, useState } from "react";
import { getAllQuizzes } from "../services/api";
import { useNavigate } from "react-router-dom";
import "../styles/quizList.css";

function QuizList() {
  const navigate = useNavigate();
  const [quizzes, setQuizzes] = useState([]);

  useEffect(() => {
    getAllQuizzes()
      .then((res) => setQuizzes(res.data))
      .catch(console.error);
  }, []);

  const goToQuestionPage = (quiz_id) => {
    navigate(`/quiz/${quiz_id}`);
  };

  return (
    <div className="quizlist-page">
      <div className="quizlist-card">
        <h2>📋 Available Quizzes</h2>
        {quizzes.length === 0 ? (
          <p>No quizzes available right now.</p>
        ) : (
          <ul className="quiz-grid">
            {quizzes.map((quiz) => (
              <li
                key={quiz.quiz_id}
                className="quiz-item"
                onClick={() => goToQuestionPage(quiz.quiz_id)}
              >
                <h3>{quiz.quiz_title}</h3>
                <p>Click to start this quiz ➡️</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default QuizList;
