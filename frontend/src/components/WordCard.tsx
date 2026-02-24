import type { PhrasalVerb } from '../types';
import './WordCard.css';

interface Props {
  word: PhrasalVerb;
  isActive: boolean;
}

export function WordCard({ word, isActive }: Props) {
  return (
    <div className={`word-card ${isActive ? 'active' : ''}`}>
      {/* 배경 이미지 (나중에 ComfyUI 생성 이미지) */}
      <div className="card-background">
        {word.assets.length > 0 ? (
          <img src={word.assets[0].url} alt={word.phrase} />
        ) : (
          <div className="placeholder-bg">
            <span className="placeholder-emoji">📚</span>
          </div>
        )}
      </div>
      
      {/* 오버레이 콘텐츠 */}
      <div className="card-content">
        <div className="phrase-section">
          <h1 className="phrase">{word.phrase}</h1>
          <p className="meaning">{word.meaning}</p>
        </div>
        
        <div className="example-section">
          <p className="example">{word.example}</p>
        </div>
        
        {/* 액션 버튼들 */}
        <div className="actions">
          <button className="action-btn">❤️</button>
          <button className="action-btn">🔊</button>
          <button className="action-btn">📖</button>
        </div>
      </div>
    </div>
  );
}
