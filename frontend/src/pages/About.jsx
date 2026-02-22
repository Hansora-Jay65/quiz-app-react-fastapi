import React from "react";
import "../styles/about.css";

function AboutPage() {
  return (
    <main className="about-page">
      <section className="about-card">
        <h1 className="about-title">What is Brain Spark?</h1>
        <p className="about-intro">
          Brain Spark is an AI‑assisted quiz platform where you can create, play, and
          analyze quizzes in a clean, fast experience.
        </p>

        <h2 className="about-section-title">What you can do</h2>
        <ul className="about-list">
          <li>
            <strong>Create quizzes</strong> with multiple questions and answers in a
            few clicks.
          </li>
          <li>
            <strong>View & manage quizzes</strong> – update existing quizzes or delete
            the ones you no longer need.
          </li>
          <li>
            <strong>Generate MCQs from PDFs</strong> using the PDF MCQ Generator to
            quickly build question sets from your study material.
          </li>
          <li>
            <strong>Track results</strong> on the leaderboard and see how different
            users perform on your quizzes.
          </li>
          <li>
            <strong>Analyze performance</strong> in the Analytics dashboard to
            understand scores, attempts, and quiz difficulty.
          </li>
        </ul>

        <h2 className="about-section-title">Who is it for?</h2>
        <p className="about-text">
          Brain Spark is designed for students, teachers, and anyone who wants to
          test knowledge or build practice questions quickly. You can use it for
          self‑practice, classroom quizzes, or interview preparation.
        </p>

        <h2 className="about-section-title">How it works</h2>
        <ol className="about-steps">
          <li>Register or sign in to your Brain Spark account.</li>
          <li>Create a new quiz or upload a PDF to generate MCQs automatically.</li>
          <li>Share the quiz or take it yourself and view your results.</li>
          <li>Use the leaderboard and analytics pages to track progress over time.</li>
        </ol>

        <p className="about-footer">
          Brain Spark aims to make learning a little more fun and a lot more
          interactive.
        </p>
      </section>
    </main>
  );
}

export default AboutPage;
