import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/quizIndex.css";

function QuizIndex() {
  const navigate = useNavigate();

  const goToCreateQuestion = () => {
    navigate("/createQuestion");
  };

  return (
    <div className="quizindex-container">
      <div className="quizindex-card">
        <h1>Quiz Index Page</h1>
        <p>Select an option to continue</p>

        <button onClick={goToCreateQuestion}>➕ Create Question</button>
      </div>
    </div>
  );
}

export default QuizIndex;
