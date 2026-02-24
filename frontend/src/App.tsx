import { useEffect } from 'react';
import { useStore } from './store/useStore';
import { ShortsViewer } from './components/ShortsViewer';
import phrasalVerbsData from '../../data/phrasal-verbs.json';
import type { PhrasalVerb } from './types';
import './App.css';

function App() {
  const { setWords, viewedWords } = useStore();

  useEffect(() => {
    // 데이터 로드 (나중에 KV API로 대체)
    setWords(phrasalVerbsData as PhrasalVerb[]);
  }, [setWords]);

  return (
    <div className="app">
      <ShortsViewer />
      
      {/* 디버그 정보 (개발용) */}
      {import.meta.env.DEV && (
        <div className="debug-info">
          <span>Viewed: {viewedWords.length}</span>
        </div>
      )}
    </div>
  );
}

export default App;
