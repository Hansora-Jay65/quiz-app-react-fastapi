import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/Navbar.css";
import brainSparkLogo from "../assets/brain-spark-logo.png";
import { useAuth } from "../components/AuthContext";

function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleToggleMenu = () => {
    setIsMenuOpen((prev) => !prev);
  };

  const handleNavLinkClick = (event, targetPath) => {
    // If user is not logged in, redirect any nav link (except Login) to /register
    if (!user) {
      event.preventDefault();
      setIsMenuOpen(false);
      navigate("/register");
      return;
    }

    // If logged in, allow normal navigation
    setIsMenuOpen(false);
  };

  const handleAuthClick = () => {
    if (user) {
      logout();
      setIsMenuOpen(false);
      navigate("/login");
    } else {
      setIsMenuOpen(false);
      navigate("/login");
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <div className="navbar-logo">
          <Link
            to="/"
            className="navbar-brand"
            onClick={(e) => handleNavLinkClick(e, "/")}
          >
            <img
              src={brainSparkLogo}
              alt="Brain Spark logo"
              className="navbar-logo-image"
            />
            <span className="navbar-logo-text">Brain Spark</span>
          </Link>
        </div>

        {/* Mobile hamburger button */}
        <button
          className="navbar-toggle"
          type="button"
          aria-label="Toggle navigation menu"
          onClick={handleToggleMenu}
        >
          <span className="navbar-toggle-bar" />
          <span className="navbar-toggle-bar" />
          <span className="navbar-toggle-bar" />
        </button>
      </div>

      <ul className={`navbar-links ${isMenuOpen ? "open" : ""}`}>
        <li>
          <Link
            to="/quizapp"
            onClick={(e) => handleNavLinkClick(e, "/quizapp")}
          >
            Home
          </Link>
        </li>
        <li>
          <Link to="/about" onClick={(e) => handleNavLinkClick(e, "/about")}>
            About
          </Link>
        </li>
        <li>
          <Link
            to="/leaderboard"
            onClick={(e) => handleNavLinkClick(e, "/leaderboard")}
          >
            Leaderboard
          </Link>
        </li>
        <li>
          <Link
            to="/createQuizPage"
            onClick={(e) => handleNavLinkClick(e, "/createQuizPage")}
          >
            Create Quiz
          </Link>
        </li>
        <li>
          <Link
            to="/pdf-mcq-generator"
            onClick={(e) => handleNavLinkClick(e, "/pdf-mcq-generator")}
          >
            PDF MCQ Generator
          </Link>
        </li>
        <li>
          <Link
            to="/analytics"
            onClick={(e) => handleNavLinkClick(e, "/analytics")}
          >
            Analytics
          </Link>
        </li>
        <li>
          <button
            type="button"
            className="navbar-auth-button"
            onClick={handleAuthClick}
          >
            {user ? "Logout" : "Login"}
          </button>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
