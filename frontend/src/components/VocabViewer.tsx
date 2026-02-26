import { useState, useRef } from 'react';
import type { TouchEvent } from 'react';
import { vocabWords } from '../data/vocabData';
import { VocabCard } from './VocabCard';
import './VocabViewer.css';

export function VocabViewer() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const touchStartY = useRef(0);
  const touchEndY = useRef(0);

  const handleTouchStart = (e: TouchEvent) => {
    touchStartY.current = e.touches[0].clientY;
  };

  const handleTouchMove = (e: TouchEvent) => {
    touchEndY.current = e.touches[0].clientY;
  };

  const handleTouchEnd = () => {
    const diff = touchStartY.current - touchEndY.current;
    const threshold = 50;

    if (diff > threshold && currentIndex < vocabWords.length - 1) {
      // 위로 스와이프 → 다음 단어
      setCurrentIndex(prev => prev + 1);
    } else if (diff < -threshold && currentIndex > 0) {
      // 아래로 스와이프 → 이전 단어
      setCurrentIndex(prev => prev - 1);
    }
  };

  const goToWord = (index: number) => {
    setCurrentIndex(index);
  };

  const currentWord = vocabWords[currentIndex];

  return (
    <div 
      className="vocab-viewer"
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
    >
      {/* 메인 카드 */}
      <div className="card-container">
        <VocabCard word={currentWord} isActive={true} />
      </div>

      {/* 사이드 네비게이션 */}
      <div className="side-nav">
        {vocabWords.map((word, idx) => (
          <button
            key={word.id}
            className={`word-dot ${idx === currentIndex ? 'active' : ''}`}
            onClick={() => goToWord(idx)}
            title={word.phrase}
          >
            <span className="word-initial">{word.phrase[0]}</span>
          </button>
        ))}
      </div>

      {/* 상단 진행률 */}
      <div className="progress-bar">
        <div 
          className="progress-fill"
          style={{ width: `${((currentIndex + 1) / vocabWords.length) * 100}%` }}
        />
      </div>

      {/* 키보드 네비게이션 (데스크톱) */}
      <div className="keyboard-nav">
        <button 
          onClick={() => currentIndex > 0 && setCurrentIndex(prev => prev - 1)}
          disabled={currentIndex === 0}
        >
          ↑ 이전
        </button>
        <span>{currentIndex + 1} / {vocabWords.length}</span>
        <button 
          onClick={() => currentIndex < vocabWords.length - 1 && setCurrentIndex(prev => prev + 1)}
          disabled={currentIndex === vocabWords.length - 1}
        >
          다음 ↓
        </button>
      </div>
    </div>
  );
}
