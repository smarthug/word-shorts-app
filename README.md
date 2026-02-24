# Word Shorts App

영어 숙어 학습 쇼츠 앱 - TikTok 스타일 스와이프 UI

## 🏗️ 프로젝트 구조

```
word-shorts-app/
├── data/
│   └── phrasal-verbs.json    # 변환된 숙어 데이터 (2236개)
├── scripts/
│   └── transform-anki.py     # Anki → JSON 변환 스크립트
├── frontend/                  # React + Vite 앱
│   ├── src/
│   │   ├── components/
│   │   │   ├── WordCard.tsx
│   │   │   ├── WordCard.css
│   │   │   ├── ShortsViewer.tsx
│   │   │   └── ShortsViewer.css
│   │   ├── store/
│   │   │   └── useStore.ts   # Zustand 상태관리
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── App.css
│   └── package.json
└── README.md
```

## 🚀 실행

```bash
cd frontend
npm install
npm run dev
```

## 📋 Phase 1 완료 (현재)

- [x] Anki JSON → KV 형식 변환
- [x] React + Vite 프로젝트 셋업
- [x] TikTok 스타일 스와이프 UI
- [x] 상태관리 (Zustand + localStorage)
- [x] 본 단어 기록

## 📋 Phase 2 (다음)

- [ ] ComfyUI 이미지 생성 파이프라인
- [ ] GPT 시나리오 생성
- [ ] Cloudflare KV + R2 연동
- [ ] 캐싱 전략 적용

## 📋 Phase 3 (향후)

- [ ] 영상 생성
- [ ] TTS 추가
- [ ] PWA 지원

## 🎮 사용법

- **스와이프 위/아래**: 다음/이전 단어
- **키보드**: ↑↓ 또는 j/k
- **하트**: 즐겨찾기 (예정)
- **스피커**: 발음 재생 (예정)
- **책**: 상세 보기 (예정)

---

*Last Updated: 2026-02-24*
