import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export const getAllQuizzes = () => API.get("/Quizzes/Quizzes/getQuizzes");

export const existUser = (email, password) =>
  API.post(
    "Users/Users/login",
    new URLSearchParams({
      username: email,
      password: password,
    })
  );

export const createUser = (email, password) =>
  API.post("Users/Users/createUser", {
    user_email: email,
    hashed_password: password,
  });

export const getQustionsByQuiz = (quiz_id) =>
  API.get(`/Questions/Questions/getQuizQuestions?quiz_id=${quiz_id}`);

export const getSubmissionsByUser = (user_id) =>
  API.get(`/Submissions/Submissions/getSubmissionByUser?user_id=${user_id}`);

export const deleteQuiz = (quiz_id) =>
  API.delete(`/Quizzes/Quizzes/deleteQuiz?quiz_id=${quiz_id}`);

export const createQuiz = (quiz_title, created_by, created_at) =>
  API.post("/Quizzes/Quizzes/createQuiz", {
    quiz_title: quiz_title,
    created_by: created_by,
    created_at: created_at,
  });

export const createQuestion = (quiz_id, questionText) =>
  API.post("/Questions/Questions/createQuestion", {
    quiz_id: quiz_id,
    question_text: questionText,
  });

export const createAnswer = (question_id, answer_text, is_correct) =>
  API.post("/Answers/Answers/createAnswer", {
    question_id: question_id,
    answer_text: answer_text,
    is_correct: is_correct,
  });

export const updateQuestion = async (quiz_id, question_text, question_id) => {
  return API.put("/Questions/Questions/editQuestion", {
    quiz_id: quiz_id,
    question_text: question_text,
    question_id: question_id,
  });
};

export const updateAnswer = async (
  question_id,
  answer_id,
  answer_text,
  answer_true
) => {
  console.log("API JS FILE", question_id, answer_id, answer_text, answer_true);
  return API.put("/Answers/Answers/editAnswer", {
    question_id: question_id,
    answer_id: answer_id,
    answer_text: answer_text,
    answer_true: answer_true,
  });
};

export const createSubmission = async (payload) => {
  return API.post("/Submissions/Submissions/createSubmission", payload);
};

export const getQuizStatistics = async (quiz_id) => {
  return API.get(`/Submissions/Submissions/getQuizStatistics?quiz_id=${quiz_id}`);
};

export const generateMCQsFromPDF = async (formData) => {
  return API.post("/PDF_MCQ/generate-mcqs-only", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

export const generateMCQsAndCreateQuiz = async (formData) => {
  return API.post("/PDF_MCQ/generate-mcqs", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};
