import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/homepage.css";  // 🔹 Import CSS

function HomePage() {
  const navigate = useNavigate();

  return (
    <main className="homepage">
      <div className="homepage-container">
        <h1 className="homepage-title">Welcome to Brain Spark</h1>
        <h2 className="homepage-subtitle">Create, take, and analyze smart quizzes</h2>

        <div className="homepage-buttons">
          <button className="btn primary" onClick={() => navigate("/register")}>
            Register
          </button>
          <button className="btn secondary" onClick={() => navigate("/login")}>
            Sign in
          </button>
        </div>
      </div>
    </main>
  );
}

export default HomePage;
