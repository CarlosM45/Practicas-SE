import { Button } from './ui/button';
import { Card } from './ui/card';
import { ArrowLeft, Home } from 'lucide-react';
import type { Question } from '../App';

type QuestionScreenProps = {
  question: Question;
  onAnswer: (answer: string) => void;
  onBack: () => void;
  onRestart: () => void;
  canGoBack: boolean;
  questionNumber: number;
  totalQuestions: number;
};

export function QuestionScreen({
  question,
  onAnswer,
  onBack,
  onRestart,
  canGoBack,
  questionNumber,
  totalQuestions,
}: QuestionScreenProps) {
  return (
    <Card className="max-w-3xl w-full p-8 shadow-xl bg-gray-800 border-gray-700">
      <div className="space-y-8">
        <div className="flex justify-between items-center">
          <span className="text-purple-400">
            Pregunta {questionNumber} de {totalQuestions}
          </span>
          <div className="h-2 flex-1 mx-4 bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-purple-500 to-blue-500 transition-all duration-300"
              style={{ width: `${(questionNumber / totalQuestions) * 100}%` }}
            />
          </div>
        </div>

        <div className="text-center">
          <h2 className="text-gray-100">{question.text}</h2>
        </div>

        <div className="grid grid-cols-1 gap-3">
          {question.options.map((option) => (
            <Button
              key={option}
              onClick={() => onAnswer(option)}
              variant="outline"
              size="lg"
              className="h-auto py-4 bg-gray-700 border-gray-600 text-gray-100 hover:bg-purple-600 hover:border-purple-500 hover:text-white transition-all"
            >
              {option}
            </Button>
          ))}
        </div>

        <div className="flex gap-3 pt-4">
          <Button
            onClick={onBack}
            variant="outline"
            disabled={!canGoBack}
            className="flex-1 gap-2 bg-gray-700 border-gray-600 text-gray-100 hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ArrowLeft className="w-4 h-4" />
            Regresar
          </Button>
          <Button
            onClick={onRestart}
            variant="outline"
            className="flex-1 gap-2 bg-gray-700 border-gray-600 text-gray-100 hover:bg-gray-600"
          >
            <Home className="w-4 h-4" />
            Volver al inicio
          </Button>
        </div>
      </div>
    </Card>
  );
}
