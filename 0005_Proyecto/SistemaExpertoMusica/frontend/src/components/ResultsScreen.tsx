import { useState, useMemo } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { ArrowUpDown, Music, Home } from 'lucide-react';
import type { Answer } from '../App';

type Song = {
  id: number;
  title: string;
  artist: string;
  popularity: number;
  genre: string;
};

type SortOption = 'title-asc' | 'title-desc' | 'artist-asc' | 'artist-desc' | 'popularity-asc' | 'popularity-desc';

type ResultsScreenProps = {
  answers: Answer[];
  onRestart: () => void;
};

const generateRecommendations = (answers: Answer[]): Song[] => {
  const songs: Song[] = [
    { id: 1, title: 'Blinding Lights', artist: 'The Weeknd', popularity: 98, genre: 'Pop' },
    { id: 2, title: 'Shape of You', artist: 'Ed Sheeran', popularity: 95, genre: 'Pop' },
    { id: 3, title: 'Bohemian Rhapsody', artist: 'Queen', popularity: 92, genre: 'Rock' },
    { id: 4, title: 'Stairway to Heaven', artist: 'Led Zeppelin', popularity: 88, genre: 'Rock' },
    { id: 5, title: 'God\'s Plan', artist: 'Drake', popularity: 94, genre: 'Hip-Hop' },
    { id: 6, title: 'HUMBLE.', artist: 'Kendrick Lamar', popularity: 90, genre: 'Hip-Hop' },
    { id: 7, title: 'One More Time', artist: 'Daft Punk', popularity: 87, genre: 'Electrónica' },
    { id: 8, title: 'Midnight City', artist: 'M83', popularity: 85, genre: 'Electrónica' },
    { id: 9, title: 'Take Five', artist: 'Dave Brubeck', popularity: 82, genre: 'Jazz' },
    { id: 10, title: 'So What', artist: 'Miles Davis', popularity: 80, genre: 'Jazz' },
    { id: 11, title: 'Levitating', artist: 'Dua Lipa', popularity: 96, genre: 'Pop' },
    { id: 12, title: 'Someone Like You', artist: 'Adele', popularity: 93, genre: 'Pop' },
  ];

  return songs.slice(0, 8);
};

export function ResultsScreen({ answers, onRestart }: ResultsScreenProps) {
  const [sortOption, setSortOption] = useState<SortOption>('popularity-desc');
  const recommendations = useMemo(() => generateRecommendations(answers), [answers]);

  const sortedRecommendations = useMemo(() => {
    const sorted = [...recommendations];
    
    switch (sortOption) {
      case 'title-asc':
        return sorted.sort((a, b) => a.title.localeCompare(b.title));
      case 'title-desc':
        return sorted.sort((a, b) => b.title.localeCompare(a.title));
      case 'artist-asc':
        return sorted.sort((a, b) => a.artist.localeCompare(b.artist));
      case 'artist-desc':
        return sorted.sort((a, b) => b.artist.localeCompare(a.artist));
      case 'popularity-asc':
        return sorted.sort((a, b) => a.popularity - b.popularity);
      case 'popularity-desc':
        return sorted.sort((a, b) => b.popularity - a.popularity);
      default:
        return sorted;
    }
  }, [recommendations, sortOption]);

  return (
    <Card className="max-w-4xl w-full p-8 shadow-xl bg-gray-800 border-gray-700">
      <div className="space-y-6">
        <div className="text-center space-y-2">
          <div className="flex justify-center">
            <div className="bg-gradient-to-br from-purple-500 to-blue-500 p-3 rounded-full">
              <Music className="w-8 h-8 text-white" />
            </div>
          </div>
          <h2 className="text-purple-400">Tus Recomendaciones</h2>
          <p className="text-gray-300">
            Basadas en tus respuestas, aquí están las mejores canciones para ti
          </p>
        </div>

        <div className="flex items-center gap-3">
          <ArrowUpDown className="w-5 h-5 text-gray-400" />
          <span className="text-gray-300">Ordenar por:</span>
          <Select value={sortOption} onValueChange={(value) => setSortOption(value as SortOption)}>
            <SelectTrigger className="w-64 bg-gray-700 border-gray-600 text-gray-100">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="bg-gray-700 border-gray-600">
              <SelectItem value="title-asc" className="text-gray-100 focus:bg-gray-600">Título (A-Z)</SelectItem>
              <SelectItem value="title-desc" className="text-gray-100 focus:bg-gray-600">Título (Z-A)</SelectItem>
              <SelectItem value="artist-asc" className="text-gray-100 focus:bg-gray-600">Artista (A-Z)</SelectItem>
              <SelectItem value="artist-desc" className="text-gray-100 focus:bg-gray-600">Artista (Z-A)</SelectItem>
              <SelectItem value="popularity-asc" className="text-gray-100 focus:bg-gray-600">Popularidad (Menor a Mayor)</SelectItem>
              <SelectItem value="popularity-desc" className="text-gray-100 focus:bg-gray-600">Popularidad (Mayor a Menor)</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
          {sortedRecommendations.map((song, index) => (
            <div
              key={song.id}
              className="flex items-center gap-4 p-4 bg-gray-700 border border-gray-600 rounded-lg hover:shadow-md hover:bg-gray-650 transition-all"
            >
              <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-purple-400 to-blue-400 rounded-full flex items-center justify-center">
                <span className="text-white">{index + 1}</span>
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-gray-100 truncate">{song.title}</h3>
                <p className="text-gray-400">{song.artist}</p>
              </div>
              <div className="flex-shrink-0 text-right">
                <div className="flex items-center gap-2">
                  <div className="w-16 h-2 bg-gray-600 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-purple-500 to-blue-500"
                      style={{ width: `${song.popularity}%` }}
                    />
                  </div>
                  <span className="text-gray-300">{song.popularity}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="pt-4">
          <Button
            onClick={onRestart}
            className="w-full gap-2 bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white"
            size="lg"
          >
            <Home className="w-5 h-5" />
            Volver al inicio
          </Button>
        </div>
      </div>
    </Card>
  );
}
