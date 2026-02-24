import { useEffect, useRef, useCallback } from 'react';
import { useStore } from '../store/useStore';
import { WordCard } from './WordCard';
import './ShortsViewer.css';

export function ShortsViewer() {
  const { words, currentIndex, setCurrentIndex, addViewedWord } = useStore();
  const containerRef = useRef<HTMLDivElement>(null);

  // 스크롤 이벤트로 현재 카드 감지
  const handleScroll = useCallback(() => {
    if (!containerRef.current) return;
    
    const container = containerRef.current;
    const scrollTop = container.scrollTop;
    const cardHeight = window.innerHeight;
    const newIndex = Math.round(scrollTop / cardHeight);
    
    if (newIndex !== currentIndex && newIndex >= 0 && newIndex < words.length) {
      setCurrentIndex(newIndex);
      addViewedWord(words[newIndex].id);
    }
  }, [currentIndex, words, setCurrentIndex, addViewedWord]);

  // 키보드 네비게이션
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!containerRef.current) return;
      
      const cardHeight = window.innerHeight;
      
      if (e.key === 'ArrowDown' || e.key === 'j') {
        e.preventDefault();
        const newIndex = Math.min(currentIndex + 1, words.length - 1);
        containerRef.current.scrollTo({
          top: newIndex * cardHeight,
          behavior: 'smooth',
        });
      } else if (e.key === 'ArrowUp' || e.key === 'k') {
        e.preventDefault();
        const newIndex = Math.max(currentIndex - 1, 0);
        containerRef.current.scrollTo({
          top: newIndex * cardHeight,
          behavior: 'smooth',
        });
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentIndex, words.length]);

  // 첫 단어 본 것으로 기록
  useEffect(() => {
    if (words.length > 0) {
      addViewedWord(words[0].id);
    }
  }, [words, addViewedWord]);

  if (words.length === 0) {
    return (
      <div className="loading">
        <p>Loading words...</p>
      </div>
    );
  }

  return (
    <div 
      ref={containerRef}
      className="shorts-viewer"
      onScroll={handleScroll}
    >
      {words.map((word, index) => (
        <WordCard
          key={word.id}
          word={word}
          isActive={index === currentIndex}
        />
      ))}
      
      {/* 프로그레스 인디케이터 */}
      <div className="progress-indicator">
        <span>{currentIndex + 1} / {words.length}</span>
      </div>
    </div>
  );
}
