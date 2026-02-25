# Word Shorts 이미지 생성 방법론 v1

> **작성일**: 2025-02-25  
> **상태**: ✅ 검증 완료  
> **스크립트**: `scripts/generate-vocab-v3.py`

---

## 📋 개요

영어 단어 학습용 이미지를 자동 생성하는 파이프라인.  
GPT가 단어에 맞는 시나리오를 생성하고, ComfyUI(Flux)가 다양한 아트 스타일로 이미지를 만든다.

### 핵심 아이디어
- **단어 → 시나리오 → 이미지** (2단계 생성)
- 하나의 단어에 **10가지 다른 상황** × **10가지 아트 스타일**
- TikTok/Shorts 형태의 세로 이미지 (9:16)

---

## 🔄 파이프라인 흐름

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: 시나리오 생성 (GPT-4o-mini)                      │
│  ─────────────────────────────────────────────────────── │
│  Input:  단어 + 뜻 + 예문                                 │
│  Output: 10개의 다양한 상황 시나리오                        │
│                                                          │
│  예시 (Replenish - 보충하다):                              │
│  1. 정원에서 화분에 흙 채우기                               │
│  2. 바에서 바텐더가 얼음 채우기                             │
│  3. 주방에서 엄마가 과일 채우기                             │
│  ...                                                     │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Step 2: 이미지 생성 (ComfyUI + Flux)                     │
│  ─────────────────────────────────────────────────────── │
│  Input:  시나리오 + 스타일 프리픽스                         │
│  Output: 10개 이미지 (각 시나리오 × 각 스타일)              │
│                                                          │
│  시나리오 1 → 지브리 스타일 → image-01-ghibli.png          │
│  시나리오 2 → 파스텔 스타일 → image-02-pastel.png          │
│  ...                                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 10가지 아트 스타일

| # | 스타일 | 영문 키 | 프롬프트 프리픽스 |
|---|--------|---------|------------------|
| 1 | 파스텔 | pastel | soft pastel colors, dreamy atmosphere |
| 2 | 애니메이션 | anime | anime style, vibrant colors, expressive |
| 3 | 지브리 | ghibli | Studio Ghibli style, whimsical, hand-drawn |
| 4 | 디즈니/픽사 | disney | Disney Pixar 3D animation style |
| 5 | 만화 | comic | comic book style, bold lines, dynamic |
| 6 | 수채화 | watercolor | watercolor painting, soft edges, artistic |
| 7 | 미니멀 | minimalist | minimalist illustration, clean lines |
| 8 | 픽셀아트 | pixel_art | pixel art, retro game style, 16-bit |
| 9 | 팝아트 | pop_art | pop art style, bold colors, Andy Warhol |
| 10 | 컨셉아트 | concept_art | concept art, detailed, professional |

### 스타일 할당 방식
- 시나리오 번호에 따라 스타일이 순환 배정
- 시나리오 1 → 스타일 리스트[0], 시나리오 2 → 스타일 리스트[1], ...

---

## 📐 기술 스펙

| 항목 | 값 |
|------|-----|
| **해상도** | 768 × 1344 (9:16 세로) |
| **모델** | Flux (via ComfyUI) |
| **LLM** | GPT-4o-mini |
| **시나리오 수** | 단어당 10개 |
| **이미지 수** | 단어당 10개 |
| **ComfyUI 포트** | 8188 (GPU 0) |

---

## 📁 파일 구조

```
/home/filadmin/word-shorts-app/
├── scripts/
│   └── generate-vocab-v3.py    # 메인 스크립트
├── data/
│   └── phrasal-verbs.json      # 2236개 구동사 데이터
└── docs/
    └── IMAGE_GENERATION_V1.md  # 이 문서

/home/filadmin/Desktop/word-shorts-output/
├── images/v3/
│   ├── replenish-01-ghibli.png
│   ├── replenish-02-pastel.png
│   └── ...
└── metadata/v3/
    ├── replenish.json
    └── ...

/home/filadmin/Desktop/word-shorts/
└── .env                        # OPENAI_API_KEY
```

---

## 🚀 사용법

### 기본 실행
```bash
cd /home/filadmin/word-shorts-app
export OPENAI_API_KEY="sk-..."
WORDS="Replenish" python3 -u scripts/generate-vocab-v3.py
```

### 여러 단어 실행
```bash
WORDS="Replenish,Pervasive,Deliberate" python3 -u scripts/generate-vocab-v3.py
```

### 옵션
- `-u` 플래그: unbuffered 출력 (실시간 진행 확인)
- 이미 존재하는 이미지는 자동 스킵

---

## 📊 테스트 결과

### 생성 완료 단어 (2025-02-25)
| 단어 | 이미지 수 | 상태 |
|------|----------|------|
| Replenish | 10 | ✅ |
| Extant | 10 | ✅ |
| Pervasive | 10 | ✅ |
| Deliberate | 10 | ✅ |

### 품질 평가
- ✅ 시나리오 다양성: 단어 의미에 맞는 다양한 상황 생성
- ✅ 스타일 품질: 10가지 스타일 모두 구분 가능
- ✅ 해상도: 모바일 최적화 (9:16)
- ⚠️ 일부 스타일 (픽셀아트)은 복잡한 장면에서 품질 저하

---

## 🔮 다음 단계 (v2 고려사항)

### 개선 아이디어
- [ ] 스타일별 품질 최적화 (프롬프트 튜닝)
- [ ] 병렬 생성 (멀티 GPU 활용)
- [ ] 예문 시각화 강화
- [ ] 텍스트 오버레이 자동화
- [ ] 비디오 생성 파이프라인

### 배치 생성
- [ ] 2236개 구동사 전체 생성
- [ ] 예상 시간: ~374시간 (단어당 ~10분)
- [ ] 멀티 GPU 병렬화로 단축 가능

---

## 📝 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| 2025-02-25 | v1.0 | 초기 문서 작성, v3 파이프라인 검증 완료 |

---

*이 문서는 Word Shorts 이미지 생성 방법론의 첫 번째 버전을 기록합니다.*
