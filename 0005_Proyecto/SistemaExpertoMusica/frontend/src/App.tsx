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

export interface Song {
  title: string;
  artist: string;
  genre: string;
  popularity: number;
}

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
    text: "¿Deseas ver recomendaciones con letra explícita? (palabras antisonantes)",
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

  const [recommendations, setRecommendations] = useState<Song[]>([]);

  const handleStart = () => {
    setScreen("questions");
    setCurrentQuestionIndex(0);
    setAnswers([]);
    setRecommendations([]);
  };

  const handleAnswer = async (answer: string) => {
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
      try{
        console.log("Enviando respuestas a Python...",newAnswers);
        const response=await fetch("http://localhost:8000/recomendar",{
          method:"POST",
          headers:{
            "Content-Type":"application/json",
          },
          body:JSON.stringify(newAnswers),
        });
        if (!response.ok){
          throw new Error("Error en la respuesta del servidor");
        }
        const data=await response.json();
        console.log("Recomendaciones recibidas:",data);
        setRecommendations(data);
        setScreen("results");
      }catch(error){
        console.error("Error conectando con el backend:",error);
        alert("Hubo un error conectando con el sistema experto. Revisa que la consola esté abierta");
      }
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
    setRecommendations([]);
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
          recommendations={recommendations}
          onRestart={handleRestart}
        />
      )}
    </div>
  );
}