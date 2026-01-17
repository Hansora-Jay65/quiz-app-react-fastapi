import React, { useState } from "react";
import { createUser } from "../services/api";
import { useNavigate } from "react-router-dom";
import "../styles/userRegistration.css";

function UserRegistration() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [passwordStrength, setPasswordStrength] = useState("");
  const [passwordStrengthLabel, setPasswordStrengthLabel] = useState("");
  const [emailError, setEmailError] = useState("");

  const evaluatePasswordStrength = (value) => {
    if (!value) {
      setPasswordStrength("");
      setPasswordStrengthLabel("");
      return;
    }

    let score = 0;

    if (value.length >= 8) score += 1;
    if (/[A-Z]/.test(value)) score += 1;
    if (/[a-z]/.test(value)) score += 1;
    if (/\d/.test(value)) score += 1;

    if (score <= 1) {
      setPasswordStrength("weak");
      setPasswordStrengthLabel("Weak (use at least 8 characters with upper, lower case and numbers)");
    } else if (score === 2 || score === 3) {
      setPasswordStrength("medium");
      setPasswordStrengthLabel("Medium (add more character types to strengthen)");
    } else {
      setPasswordStrength("strong");
      setPasswordStrengthLabel("Strong password");
    }
  };

  const validateEmail = (value) => {
    if (!value) return "Email is required";
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(value) ? "" : "Enter a valid email address";
  };

  const handleRegister = async (e) => {
    e.preventDefault(); // prevent page reload

    const emailErr = validateEmail(email);
    setEmailError(emailErr);

    if (!email || !password || emailErr) {
      setMessage("⚠️ Please fill out all fields correctly.");
      return;
    }

    // Basic client-side check consistent with backend rules
    const lengthOk = password.length >= 8;
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);

    if (!lengthOk || !hasUpper || !hasLower || !hasNumber) {
      setMessage(
        "⚠️ Password must be at least 8 characters and include uppercase, lowercase letters and numbers."
      );
      return;
    }

    try {
      const res = await createUser(email, password);
      if (res.data.User === "User Created") {
        setMessage("✅ User registered successfully!");
        setTimeout(() => navigate("/quizApp"), 1000);
      } else {
        setMessage("❌ Registration failed. Try again.");
      }
    } catch (err) {
      console.error(err);
      setMessage("🚨 Something went wrong. Please try later.");
    }
  };

  return (
    <div className="register-page">
      <form className="register-form" onSubmit={handleRegister}>
        <h1>Create Account</h1>

        <label>Email Address:</label>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => {
            const value = e.target.value;
            setEmail(value);
            setEmailError(validateEmail(value));
          }}
          className={emailError ? "error" : ""}
          required
        />
        {emailError && <p className="field-error">{emailError}</p>}

        <label>Password:</label>
        <input
          type="password"
          placeholder="Create a password"
          value={password}
          onChange={(e) => {
            const value = e.target.value;
            setPassword(value);
            evaluatePasswordStrength(value);
          }}
          required
        />

        {passwordStrength && (
          <div className="password-strength">
            <div className={`strength-bar ${passwordStrength}`}></div>
            <span className="strength-label">{passwordStrengthLabel}</span>
          </div>
        )}

        <button type="submit" className="btn primary">Register</button>

        {message && <p className="message">{message}</p>}
      </form>
    </div>
  );
}

export default UserRegistration;
