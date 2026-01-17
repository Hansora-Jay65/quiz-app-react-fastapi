import React, { useState } from "react";
import { createQuiz } from "../services/api";
import { useNavigate } from "react-router-dom";
import { useToast } from "../components/ToastContext";
import "../styles/createQuiz.css";

function CreateQuiz() {
  const navigate = useNavigate();
  const [quizTitle, setQuizTitle] = useState("");
  const [creatorName, setCreatorName] = useState("");
  const [date, setDate] = useState(new Date().toISOString().split("T")[0]);
  const [successMessage, setSuccessMessage] = useState("");
  const { showToast } = useToast();

  const handleCreationQuiz = async () => {
    try {
      const res = await createQuiz(quizTitle, creatorName, date);
      if (res.data.quiz_id !== 0) {
        setSuccessMessage("✅ Quiz Created Successfully!");

        // Reset fields
        setQuizTitle("");
        setCreatorName("");
        setDate(new Date().toISOString().split("T")[0]);

        // Optional redirect after 2s
        setTimeout(() => navigate("/newQuizIndexPage"), 2000);
      } else {
        showToast({
          type: "warning",
          message: "Quiz was not created. Please try again.",
        });
      }
    } catch (err) {
      console.error("Error creating quiz:", err);
      showToast({
        type: "error",
        message: "Error creating quiz. Please check your input and try again.",
      });
    }
  };

  return (
    <div className="createquiz-container">
      <div className="createquiz-card">
        <h1>Create a New Quiz</h1>

        <label>Quiz Title:</label>
        <input
          type="text"
          value={quizTitle}
          placeholder="Enter title of Quiz"
          onChange={(e) => setQuizTitle(e.target.value)}
        />

        <label>Created By:</label>
        <input
          type="text"
          value={creatorName}
          placeholder="Enter Creator Name"
          onChange={(e) => setCreatorName(e.target.value)}
        />

        <label>Date:</label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />

        <button onClick={handleCreationQuiz}>Create Quiz</button>

        {successMessage && <p className="success-msg">{successMessage}</p>}
      </div>
    </div>
  );
}

export default CreateQuiz;
