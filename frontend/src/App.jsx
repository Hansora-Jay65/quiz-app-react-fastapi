// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ToastProvider } from "./components/ToastContext";
import { AuthProvider } from "./components/AuthContext";
import "./styles/toast.css";
import QuizList from "./pages/QuizList";
import UserLogin from "./pages/User_Login";
import HomePage from "./pages/home";
import QuizHomePage from "./pages/Quiz_App";
import UserRegistration from "./pages/User_Registration";
import AboutPage from "./pages/About";
import Question from "./pages/Question_Of_Quiz";
import CreateQuiz from "./pages/Create_Quiz";
import CreateQuestion from "./pages/Create_Question";
import QuizIndex from "./pages/Quiz_Index";
import UpdateQuizQuestion from "./pages/Update_Question";
import DeleteQuiz from "./pages/Delete_Quiz";
import ResultPage from "./pages/Submission";
import Leaderboard from "./pages/LeaderBoard_Of_User";
import Navbar from "./pages/Navbar";
import PDF_MCQ_Generator from "./pages/PDF_MCQ_Generator";
import AnalyticsDashboard from "./pages/Analytics_Dashboard";

function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <Router>
          <Navbar></Navbar>
          <Routes>
            <Route path="/" element={<HomePage></HomePage>}></Route>
            <Route path="/login" element={<UserLogin></UserLogin>}></Route>
            <Route
              path="/register"
              element={<UserRegistration></UserRegistration>}
            ></Route>
            <Route path="/about" element={<AboutPage />} />
            <Route
              path="/quizApp"
              element={<QuizHomePage></QuizHomePage>}
            ></Route>
            <Route path="/quizList" element={<QuizList></QuizList>}></Route>
            <Route path="/quiz/:quizId" element={<Question></Question>}></Route>
            <Route
              path="/createQuizPage"
              element={<CreateQuiz></CreateQuiz>}
            ></Route>
            <Route
              path="/newQuizIndexPage"
              element={<QuizIndex></QuizIndex>}
            ></Route>
            <Route
              path="/createQuestion"
              element={<CreateQuestion></CreateQuestion>}
            ></Route>
            <Route
              path="/updateQuizQuestionAnswer"
              element={<UpdateQuizQuestion></UpdateQuizQuestion>}
            ></Route>
            <Route
              path="/deleteQuiz"
              element={<DeleteQuiz></DeleteQuiz>}
            ></Route>
            <Route path="/result/:quizId" element={<ResultPage />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route
              path="/pdf-mcq-generator"
              element={<PDF_MCQ_Generator />}
            />
            <Route
              path="/analytics"
              element={<AnalyticsDashboard />}
            />
          </Routes>
        </Router>
      </ToastProvider>
    </AuthProvider>
  );
}

export default App;
