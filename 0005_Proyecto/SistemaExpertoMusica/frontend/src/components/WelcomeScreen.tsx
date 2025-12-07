import { Button } from './ui/button';
import { Card } from './ui/card';
import { Music } from 'lucide-react';

type WelcomeScreenProps = {
  onStart: () => void;
};

export function WelcomeScreen({ onStart }: WelcomeScreenProps) {
  return (
    <Card className="max-w-2xl w-full p-8 shadow-xl bg-gray-800 border-gray-700">
      <div className="flex flex-col items-center text-center space-y-6">
        <div className="bg-gradient-to-br from-purple-500 to-blue-500 p-4 rounded-full">
          <Music className="w-12 h-12 text-white" />
        </div>
        
        <h1 className="text-purple-400">Recomendador de Música</h1>
        
        <p className="text-gray-300 max-w-md">
          Descubre nuevas canciones personalizadas basadas en tus gustos y estado de ánimo. 
          Responde algunas preguntas rápidas y recibe recomendaciones perfectas para ti.
        </p>
        
        <Button 
          onClick={onStart} 
          size="lg"
          className="bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white px-8"
        >
          Comenzar
        </Button>
      </div>
    </Card>
  );
}
