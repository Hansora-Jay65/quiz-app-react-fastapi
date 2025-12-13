import React, { createContext, useContext, useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null); // { id, email } or null

  // Load from localStorage once on mount
  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      try {
        const decoded = jwtDecode(storedToken);
        setToken(storedToken);
        setUser({ id: decoded.user_id, email: decoded.sub });
      } catch (err) {
        console.error("Failed to decode stored token", err);
        localStorage.removeItem("token");
        localStorage.removeItem("user_id");
        localStorage.removeItem("user_email");
      }
    }
  }, []);

  const login = (newToken) => {
    try {
      const decoded = jwtDecode(newToken);
      setToken(newToken);
      setUser({ id: decoded.user_id, email: decoded.sub });
      localStorage.setItem("token", newToken);
      localStorage.setItem("user_id", decoded.user_id);
      localStorage.setItem("user_email", decoded.sub);
    } catch (err) {
      console.error("Failed to decode login token", err);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_email");
  };

  return (
    <AuthContext.Provider value={{ token, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
}
