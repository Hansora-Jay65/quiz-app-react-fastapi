import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  generateMCQsFromPDF,
  generateMCQsAndCreateQuiz,
} from "../services/api";
import "../styles/pdfMCQGenerator.css";

function PDF_MCQ_Generator() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [numQuestions, setNumQuestions] = useState(5);
  const [quizTitle, setQuizTitle] = useState("");
  const [creatorName, setCreatorName] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [generatedMCQs, setGeneratedMCQs] = useState(null);
  const [createQuizMode, setCreateQuizMode] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type !== "application/pdf") {
        setMessage("❌ Please select a PDF file");
        return;
      }
      setFile(selectedFile);
      setMessage("");
    }
  };

  const handleGenerateOnly = async () => {
    if (!file) {
      setMessage("⚠️ Please select a PDF file");
      return;
    }

    setLoading(true);
    setMessage(
      "🔄 Processing PDF and generating MCQs... This may take a moment."
    );

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("num_questions", numQuestions);

      const res = await generateMCQsFromPDF(formData);
      setGeneratedMCQs(res.data);
      setMessage("✅ MCQs generated successfully!");
    } catch (err) {
      console.error("Error generating MCQs:", err);
      setMessage(
        `❌ Error: ${err.response?.data?.detail || err.message || "Failed to generate MCQs"}`
      );
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAndCreateQuiz = async () => {
    if (!file) {
      setMessage("⚠️ Please select a PDF file");
      return;
    }
    if (!quizTitle || !creatorName) {
      setMessage("⚠️ Please fill in quiz title and creator name");
      return;
    }

    setLoading(true);
    setMessage("🔄 Processing PDF, generating MCQs, and creating quiz...");

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("num_questions", numQuestions);
      formData.append("quiz_title", quizTitle);
      formData.append("created_by", creatorName);

      const res = await generateMCQsAndCreateQuiz(formData);

      if (res.data.quiz_created) {
        setMessage(
          `✅ Quiz created successfully! Quiz ID: ${res.data.quiz_id}`
        );
        setGeneratedMCQs(res.data);
        setTimeout(() => {
          navigate("/quizList");
        }, 2000);
      } else {
        setMessage(
          `⚠️ MCQs generated but quiz creation failed: ${res.data.error}`
        );
        setGeneratedMCQs(res.data);
      }
    } catch (err) {
      console.error("Error:", err);
      setMessage(
        `❌ Error: ${err.response?.data?.detail || err.message || "Failed to process request"}`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="pdf-mcq-container">
      <div className="pdf-mcq-card">
        <h1>📄 PDF to MCQ Generator</h1>
        <p className="subtitle">
          Upload a PDF file and automatically generate multiple choice questions
        </p>

        <div className="upload-section">
          <label>Select PDF File:</label>
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            disabled={loading}
          />
          {file && <p className="file-info">📎 Selected: {file.name}</p>}
        </div>

        <div className="form-group">
          <label>Number of Questions:</label>
          <input
            type="number"
            min="1"
            max="20"
            value={numQuestions}
            onChange={(e) => setNumQuestions(parseInt(e.target.value) || 5)}
            disabled={loading}
          />
        </div>

        <div className="mode-toggle">
          <button
            className={`mode-btn ${!createQuizMode ? "active" : ""}`}
            onClick={() => setCreateQuizMode(false)}
            disabled={loading}
          >
            Generate MCQs Only
          </button>
          <button
            className={`mode-btn ${createQuizMode ? "active" : ""}`}
            onClick={() => setCreateQuizMode(true)}
            disabled={loading}
          >
            Generate & Create Quiz
          </button>
        </div>

        {createQuizMode && (
          <div className="quiz-details">
            <div className="form-group">
              <label>Quiz Title:</label>
              <input
                type="text"
                value={quizTitle}
                onChange={(e) => setQuizTitle(e.target.value)}
                placeholder="Enter quiz title"
                disabled={loading}
              />
            </div>
            <div className="form-group">
              <label>Created By:</label>
              <input
                type="text"
                value={creatorName}
                onChange={(e) => setCreatorName(e.target.value)}
                placeholder="Enter creator name"
                disabled={loading}
              />
            </div>
          </div>
        )}

        {loading && (
          <div className="loading-inline">
            <span className="spinner" />
            <span className="loading-text">Processing, please wait...</span>
          </div>
        )}

        <div className="button-group">
          {!createQuizMode ? (
            <button
              className="btn primary"
              onClick={handleGenerateOnly}
              disabled={loading || !file}
            >
              {loading ? "⏳ Generating..." : "✨ Generate MCQs"}
            </button>
          ) : (
            <button
              className="btn primary"
              onClick={handleGenerateAndCreateQuiz}
              disabled={loading || !file}
            >
              {loading ? "⏳ Processing..." : "🚀 Generate & Create Quiz"}
            </button>
          )}
        </div>

        {message && (
          <p
            className={`message ${message.includes("✅") ? "success" : message.includes("⚠️") ? "warning" : "error"}`}
          >
            {message}
          </p>
        )}

        {generatedMCQs && generatedMCQs.questions && (
          <div className="results-section">
            <h2>📋 Generated Questions ({generatedMCQs.num_questions})</h2>
            <div className="questions-list">
              {generatedMCQs.questions.map((mcq, idx) => (
                <div key={idx} className="question-card">
                  <h3>Question {idx + 1}</h3>
                  <p className="question-text">{mcq.question_text}</p>
                  <ul className="answers-list">
                    {mcq.answers.map((answer, ansIdx) => (
                      <li
                        key={ansIdx}
                        className={answer.is_correct ? "correct-answer" : ""}
                      >
                        {String.fromCharCode(65 + ansIdx)}. {answer.answer_text}
                        {answer.is_correct && " ✓"}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default PDF_MCQ_Generator;
