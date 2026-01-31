import React from "react";
import { Link } from "react-router-dom";
import "../styles/Navbar.css";
import brainSparkLogo from "../assets/brain-spark-logo.png";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/" className="navbar-brand">
          <img
            src={brainSparkLogo}
            alt="Brain Spark logo"
            className="navbar-logo-image"
          />
          <span className="navbar-logo-text">Brain Spark</span>
        </Link>
      </div>

      <ul className="navbar-links">
        <li>
          <Link to="/quizapp">Home</Link>
        </li>
        <li>
          <Link to="/about">About</Link>
        </li>
        <li>
          <Link to="/leaderboard">Leaderboard</Link>
        </li>
        <li>
          <Link to="/createQuizPage">Create Quiz</Link>
        </li>
        <li>
          <Link to="/pdf-mcq-generator">PDF MCQ Generator</Link>
        </li>
        <li>
          <Link to="/analytics">Analytics</Link>
        </li>
        <li>
          <Link to="/login">Login</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
