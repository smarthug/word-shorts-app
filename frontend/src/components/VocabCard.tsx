import { useState } from 'react';
import { getImageUrl } from '../data/vocabData';
import type { VocabWord } from '../data/vocabData';
import './VocabCard.css';

interface Props {
  word: VocabWord;
  isActive: boolean;
}

const styleNames: Record<string, string> = {
  watercolor: '수채화',
  comic: '만화',
  ghibli: '지브리',
  pastel: '파스텔',
  pop_art: '팝아트',
  anime: '애니메이션',
  disney: '디즈니',
  minimalist: '미니멀',
  concept_art: '컨셉아트',
  pixel_art: '픽셀아트',
};

export function VocabCard({ word, isActive }: Props) {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  const currentImage = word.images[currentImageIndex];
  const imageUrl = getImageUrl(word.id, currentImage.file);

  const nextImage = () => {
    setImageLoaded(false);
    setCurrentImageIndex((prev) => (prev + 1) % word.images.length);
  };

  const prevImage = () => {
    setImageLoaded(false);
    setCurrentImageIndex((prev) => (prev - 1 + word.images.length) % word.images.length);
  };

  return (
    <div className={`vocab-card ${isActive ? 'active' : ''}`}>
      {/* 배경 이미지 */}
      <div className="card-background">
        {!imageError ? (
          <>
            <img 
              src={imageUrl} 
              alt={`${word.phrase} - ${currentImage.style}`}
              onLoad={() => setImageLoaded(true)}
              onError={() => setImageError(true)}
              className={imageLoaded ? 'loaded' : ''}
            />
            {!imageLoaded && (
              <div className="loading-spinner">
                <span>🎨</span>
              </div>
            )}
          </>
        ) : (
          <div className="placeholder-bg">
            <span className="placeholder-emoji">📚</span>
            <p>이미지 로딩 실패</p>
          </div>
        )}
      </div>

      {/* 스타일 네비게이션 */}
      <div className="style-nav">
        <button onClick={prevImage} className="nav-btn">◀</button>
        <span className="style-badge">
          {styleNames[currentImage.style] || currentImage.style}
          <small>{currentImageIndex + 1}/{word.images.length}</small>
        </span>
        <button onClick={nextImage} className="nav-btn">▶</button>
      </div>

      {/* 오버레이 콘텐츠 */}
      <div className="card-content">
        <div className="phrase-section">
          <h1 className="phrase">{word.phrase}</h1>
          <p className="meaning-en">{word.meaningEn}</p>
          <p className="meaning-kr">{word.meaning}</p>
        </div>
        
        <div className="example-section">
          <p className="example">"{word.example}"</p>
        </div>
      </div>

      {/* 스타일 인디케이터 (하단 점) */}
      <div className="style-dots">
        {word.images.map((_, idx) => (
          <button
            key={idx}
            className={`dot ${idx === currentImageIndex ? 'active' : ''}`}
            onClick={() => {
              setImageLoaded(false);
              setCurrentImageIndex(idx);
            }}
          />
        ))}
      </div>
    </div>
  );
}
