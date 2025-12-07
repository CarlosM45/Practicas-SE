import { useState } from "react";
import { WelcomeScreen } from "./components/WelcomeScreen";
import { QuestionScreen } from "./components/QuestionScreen";
import { ResultsScreen } from "./components/ResultsScreen";

export type Answer = {
  questionId: number;
  answer: string;
};

export type Question = {
  id: number;
  text: string;
  options: string[];
};

const questions: Question[] = [
  {
    id: 1,
    text: "¿Cómo te sientes hoy?",
    options: ["Feliz y energético", "Relajado", "Melancólico"],
  },
  {
    id: 2,
    text: "¿Qué géneros musicales prefieres?",
    options: [
      "Pop",
      "Rock",
      "Hip-Hop/Rap",
      "Electrónica",
      "Anime",
    ],
  },
  {
    id: 3,
    text: "¿Qué nivel de popularidad buscas en las canciones?",
    options: [
      "Quiero conocer música poco popular",
      "Quiero escuchar música popular",
      "Quiero escuchar música muy popular",
    ],
  },
  {
    id: 4,
    text: "¿Deseas ver recomendaciones con letra explícita?",
    options: ["Sí", "No"],
  },
];

export default function App() {
  const [screen, setScreen] = useState<
    "welcome" | "questions" | "results"
  >("welcome");
  const [currentQuestionIndex, setCurrentQuestionIndex] =
    useState(0);
  const [answers, setAnswers] = useState<Answer[]>([]);

  const handleStart = () => {
    setScreen("questions");
    setCurrentQuestionIndex(0);
    setAnswers([]);
  };

  const handleAnswer = (answer: string) => {
    const newAnswers = [
      ...answers,
      {
        questionId: questions[currentQuestionIndex].id,
        answer,
      },
    ];
    setAnswers(newAnswers);

    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      setScreen("results");
    }
  };

  const handleBack = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
      setAnswers(answers.slice(0, -1));
    }
  };

  const handleRestart = () => {
    setScreen("welcome");
    setCurrentQuestionIndex(0);
    setAnswers([]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-800 to-gray-900 flex items-center justify-center p-4">
      {screen === "welcome" && (
        <WelcomeScreen onStart={handleStart} />
      )}
      {screen === "questions" && (
        <QuestionScreen
          question={questions[currentQuestionIndex]}
          onAnswer={handleAnswer}
          onBack={handleBack}
          onRestart={handleRestart}
          canGoBack={currentQuestionIndex > 0}
          questionNumber={currentQuestionIndex + 1}
          totalQuestions={questions.length}
        />
      )}
      {screen === "results" && (
        <ResultsScreen
          answers={answers}
          onRestart={handleRestart}
        />
      )}
    </div>
  );
}