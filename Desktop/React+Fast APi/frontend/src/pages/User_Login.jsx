import React, { useState } from "react";
import { existUser } from "../services/api";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../components/AuthContext";
import "../styles/userLogin.css";

function UserLogin() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const validateEmail = (value) => {
    if (!value) return "Email is required";
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(value) ? "" : "Enter a valid email address";
  };

  const validatePassword = (value) => {
    if (!value) return "Password is required";
    if (value.length < 6) return "Password should be at least 6 characters";
    return "";
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    const emailErr = validateEmail(email);
    const passErr = validatePassword(password);

    setEmailError(emailErr);
    setPasswordError(passErr);

    if (emailErr || passErr) {
      setMessage("⚠️ Please fix the highlighted fields.");
      return;
    }

    try {
      const res = await existUser(email, password);
      const token = res.data.access_token;

      // Update global auth state and persist to localStorage
      login(token);

      setMessage("✅ Login successful!");
      setTimeout(() => navigate("/quizapp"), 1000);
    } catch (err) {
      console.error("Login failed:", err.response?.data || err.message);
      setMessage("❌ Invalid credentials. Please try again.");
    }
  };

  return (
    <div className="login-page">
      <form className="login-form" onSubmit={handleLogin}>
        <h1>Sign In</h1>

        <label>Email:</label>
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
          placeholder="Enter your password"
          value={password}
          onChange={(e) => {
            const value = e.target.value;
            setPassword(value);
            setPasswordError(validatePassword(value));
          }}
          className={passwordError ? "error" : ""}
          required
        />
        {passwordError && <p className="field-error">{passwordError}</p>}

        <button type="submit" className="btn primary">Login</button>

        {message && <p className="message">{message}</p>}
      </form>
    </div>
  );
}

export default UserLogin;
