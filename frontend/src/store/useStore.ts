import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { PhrasalVerb } from '../types';

interface AppState {
  // 본 단어 기록
  viewedWords: string[];
  addViewedWord: (id: string) => void;
  
  // 현재 인덱스
  currentIndex: number;
  setCurrentIndex: (index: number) => void;
  
  // 데이터
  words: PhrasalVerb[];
  setWords: (words: PhrasalVerb[]) => void;
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      viewedWords: [],
      addViewedWord: (id) =>
        set((state) => ({
          viewedWords: [...new Set([...state.viewedWords, id])],
        })),
      
      currentIndex: 0,
      setCurrentIndex: (index) => set({ currentIndex: index }),
      
      words: [],
      setWords: (words) => set({ words }),
    }),
    {
      name: 'word-shorts-storage',
      partialize: (state) => ({ viewedWords: state.viewedWords }),
    }
  )
);
