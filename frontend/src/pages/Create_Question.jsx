import React, { useEffect, useState } from "react";
import { getAllQuizzes, createQuestion, createAnswer } from "../services/api";
import { useToast } from "../components/ToastContext";
import { useNavigate } from "react-router-dom";
import "../styles/createQuestion.css";

function CreateQuestion() {
  const navigate = useNavigate();
  const [quizzes, setQuizzes] = useState([]);
  const [selectedQuizId, setSelectedQuizId] = useState("");
  const [questionText, setQuestionText] = useState("");
  const [answers, setAnswers] = useState(["", "", "", ""]);
  const [correctIndex, setCorrectIndex] = useState(null);
  const { showToast } = useToast();

  useEffect(() => {
    getAllQuizzes()
      .then((res) => setQuizzes(res.data))
      .catch(console.error);
  }, []);

  const handleAnswerChange = (index, value) => {
    const newAnswers = [...answers];
    newAnswers[index] = value;
    setAnswers(newAnswers);
  };

  const resetForm = () => {
    setQuestionText("");
    setAnswers(["", "", "", ""]);
    setCorrectIndex(null);
  };

  const handleSubmit = async (navigateHome = false) => {
    if (!selectedQuizId || !questionText || correctIndex === null) {
      showToast({
        type: "warning",
        message: "Please fill all fields and select the correct answer.",
      });
      return;
    }
    try {
      const qRes = await createQuestion(selectedQuizId, questionText);
      const question_id = qRes.data.Question.question_id;

      await Promise.all(
        answers.map((ans, idx) =>
          createAnswer(question_id, ans, idx === correctIndex)
        )
      );

      showToast({
        type: "success",
        message: "Question and answers created successfully.",
      });

      if (navigateHome) {
        navigate("/");
      } else {
        resetForm();
      }
    } catch (err) {
      console.error(err);
      showToast({
        type: "error",
        message: "Failed to create question or answers. Please try again.",
      });
    }
  };

  return (
    <div className="create-question-container">
      <div className="create-question-card">
        <h1>Create Question Page</h1>

        <label>Quiz:</label>
        <select
          onChange={(e) => setSelectedQuizId(e.target.value)}
          value={selectedQuizId}
        >
          <option disabled value="">
            Select Quiz
          </option>
          {quizzes.map((quiz) => (
            <option key={quiz.quiz_id} value={quiz.quiz_id}>
              {quiz.quiz_title}
            </option>
          ))}
        </select>

        <label>Question Text:</label>
        <input
          type="text"
          value={questionText}
          onChange={(e) => setQuestionText(e.target.value)}
          placeholder="Enter your question here"
        />

        <h2>Answer Options</h2>
        <ul>
          {["A", "B", "C", "D"].map((label, idx) => (
            <li key={idx}>
              Option {label}:{" "}
              <input
                type="text"
                value={answers[idx]}
                onChange={(e) => handleAnswerChange(idx, e.target.value)}
                placeholder={`Enter option ${label}`}
              />
              <input
                type="radio"
                name="correctAnswer"
                checked={correctIndex === idx}
                onChange={() => setCorrectIndex(idx)}
              />{" "}
              Correct
            </li>
          ))}
        </ul>

        <div>
          <button
            className="secondary-btn"
            onClick={() => handleSubmit(false)}
          >
            ➕ Add Another Question
          </button>
          <button
            onClick={() => handleSubmit(true)}
            style={{ marginLeft: "10px" }}
          >
            ✅ Finish & Go Home
          </button>
        </div>
      </div>
    </div>
  );
}

export default CreateQuestion;
