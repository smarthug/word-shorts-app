// Worker API URL
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://word-shorts-api.kirklayer6590.workers.dev';

// 10개 단어 데이터
export const vocabWords = [
  {
    id: 'replenish',
    phrase: 'Replenish',
    meaning: '보충하다, 다시 채우다',
    meaningEn: 'to fill or supply again',
    example: 'We need to replenish our supplies before the next trip.',
    images: [
      { style: 'watercolor', file: 'replenish-01-watercolor.png' },
      { style: 'comic', file: 'replenish-02-comic.png' },
      { style: 'ghibli', file: 'replenish-03-ghibli.png' },
      { style: 'pastel', file: 'replenish-04-pastel.png' },
      { style: 'pop_art', file: 'replenish-05-pop_art.png' },
      { style: 'anime', file: 'replenish-06-anime.png' },
      { style: 'disney', file: 'replenish-07-disney.png' },
      { style: 'minimalist', file: 'replenish-08-minimalist.png' },
      { style: 'concept_art', file: 'replenish-09-concept_art.png' },
      { style: 'pixel_art', file: 'replenish-10-pixel_art.png' },
    ]
  },
  {
    id: 'instigate',
    phrase: 'Instigate',
    meaning: '선동하다, 부추기다',
    meaningEn: 'to cause or encourage to happen',
    example: 'He was accused of trying to instigate a riot.',
    images: [
      { style: 'comic', file: 'instigate-01-comic.png' },
      { style: 'pastel', file: 'instigate-02-pastel.png' },
      { style: 'minimalist', file: 'instigate-03-minimalist.png' },
      { style: 'watercolor', file: 'instigate-04-watercolor.png' },
      { style: 'ghibli', file: 'instigate-05-ghibli.png' },
      { style: 'anime', file: 'instigate-06-anime.png' },
      { style: 'concept_art', file: 'instigate-07-concept_art.png' },
      { style: 'disney', file: 'instigate-08-disney.png' },
      { style: 'pop_art', file: 'instigate-09-pop_art.png' },
      { style: 'pixel_art', file: 'instigate-10-pixel_art.png' },
    ]
  },
  {
    id: 'substantiate',
    phrase: 'Substantiate',
    meaning: '입증하다, 실증하다',
    meaningEn: 'to provide evidence to prove',
    example: 'Can you substantiate your claims with evidence?',
    images: [
      { style: 'disney', file: 'substantiate-01-disney.png' },
      { style: 'pastel', file: 'substantiate-02-pastel.png' },
      { style: 'minimalist', file: 'substantiate-03-minimalist.png' },
      { style: 'pop_art', file: 'substantiate-04-pop_art.png' },
      { style: 'pixel_art', file: 'substantiate-05-pixel_art.png' },
      { style: 'comic', file: 'substantiate-06-comic.png' },
      { style: 'concept_art', file: 'substantiate-07-concept_art.png' },
      { style: 'ghibli', file: 'substantiate-08-ghibli.png' },
      { style: 'watercolor', file: 'substantiate-09-watercolor.png' },
      { style: 'anime', file: 'substantiate-10-anime.png' },
    ]
  },
  {
    id: 'deliberate',
    phrase: 'Deliberate',
    meaning: '신중한, 고의적인; 숙고하다',
    meaningEn: 'done intentionally; to think carefully',
    example: 'It was a deliberate attempt to mislead the public.',
    images: [
      { style: 'comic', file: 'deliberate-01-comic.png' },
      { style: 'anime', file: 'deliberate-02-anime.png' },
      { style: 'pixel_art', file: 'deliberate-03-pixel_art.png' },
      { style: 'pastel', file: 'deliberate-04-pastel.png' },
      { style: 'concept_art', file: 'deliberate-05-concept_art.png' },
      { style: 'watercolor', file: 'deliberate-06-watercolor.png' },
      { style: 'ghibli', file: 'deliberate-07-ghibli.png' },
      { style: 'pop_art', file: 'deliberate-08-pop_art.png' },
      { style: 'minimalist', file: 'deliberate-09-minimalist.png' },
      { style: 'disney', file: 'deliberate-10-disney.png' },
    ]
  },
  {
    id: 'strenuous',
    phrase: 'Strenuous',
    meaning: '격렬한, 힘든',
    meaningEn: 'requiring great effort or energy',
    example: 'The hike was more strenuous than we expected.',
    images: [
      { style: 'anime', file: 'strenuous-01-anime.png' },
      { style: 'minimalist', file: 'strenuous-02-minimalist.png' },
      { style: 'concept_art', file: 'strenuous-03-concept_art.png' },
      { style: 'pop_art', file: 'strenuous-04-pop_art.png' },
      { style: 'disney', file: 'strenuous-05-disney.png' },
      { style: 'pixel_art', file: 'strenuous-06-pixel_art.png' },
      { style: 'comic', file: 'strenuous-07-comic.png' },
      { style: 'watercolor', file: 'strenuous-08-watercolor.png' },
      { style: 'ghibli', file: 'strenuous-09-ghibli.png' },
      { style: 'pastel', file: 'strenuous-10-pastel.png' },
    ]
  },
  {
    id: 'conjunction',
    phrase: 'Conjunction',
    meaning: '결합, 접속사',
    meaningEn: 'a combination; connecting word',
    example: 'The conjunction of these events led to the discovery.',
    images: [
      { style: 'pastel', file: 'conjunction-01-pastel.png' },
      { style: 'pop_art', file: 'conjunction-02-pop_art.png' },
      { style: 'concept_art', file: 'conjunction-03-concept_art.png' },
      { style: 'ghibli', file: 'conjunction-04-ghibli.png' },
      { style: 'watercolor', file: 'conjunction-05-watercolor.png' },
      { style: 'minimalist', file: 'conjunction-06-minimalist.png' },
      { style: 'disney', file: 'conjunction-07-disney.png' },
      { style: 'comic', file: 'conjunction-08-comic.png' },
      { style: 'pixel_art', file: 'conjunction-09-pixel_art.png' },
      { style: 'anime', file: 'conjunction-10-anime.png' },
    ]
  },
  {
    id: 'extant',
    phrase: 'Extant',
    meaning: '현존하는, 남아있는',
    meaningEn: 'still existing; not destroyed',
    example: 'Only a few copies of the manuscript are extant.',
    images: [
      { style: 'disney', file: 'extant-01-disney.png' },
      { style: 'watercolor', file: 'extant-02-watercolor.png' },
      { style: 'comic', file: 'extant-03-comic.png' },
      { style: 'ghibli', file: 'extant-04-ghibli.png' },
      { style: 'anime', file: 'extant-05-anime.png' },
      { style: 'minimalist', file: 'extant-06-minimalist.png' },
      { style: 'pixel_art', file: 'extant-07-pixel_art.png' },
      { style: 'concept_art', file: 'extant-08-concept_art.png' },
      { style: 'pop_art', file: 'extant-09-pop_art.png' },
      { style: 'pastel', file: 'extant-10-pastel.png' },
    ]
  },
  {
    id: 'sedentary',
    phrase: 'Sedentary',
    meaning: '앉아서 하는, 주로 앉아 있는',
    meaningEn: 'involving much sitting; inactive',
    example: 'A sedentary lifestyle can lead to health problems.',
    images: [
      { style: 'pop_art', file: 'sedentary-01-pop_art.png' },
      { style: 'ghibli', file: 'sedentary-02-ghibli.png' },
      { style: 'watercolor', file: 'sedentary-03-watercolor.png' },
      { style: 'concept_art', file: 'sedentary-04-concept_art.png' },
      { style: 'minimalist', file: 'sedentary-05-minimalist.png' },
      { style: 'comic', file: 'sedentary-06-comic.png' },
      { style: 'anime', file: 'sedentary-07-anime.png' },
      { style: 'pastel', file: 'sedentary-08-pastel.png' },
      { style: 'disney', file: 'sedentary-09-disney.png' },
      { style: 'pixel_art', file: 'sedentary-10-pixel_art.png' },
    ]
  },
  {
    id: 'invoke',
    phrase: 'Invoke',
    meaning: '호출하다, 발동하다',
    meaningEn: 'to call upon; to cite as authority',
    example: 'The lawyer invoked the Fifth Amendment.',
    images: [
      { style: 'disney', file: 'invoke-01-disney.png' },
      { style: 'comic', file: 'invoke-02-comic.png' },
      { style: 'ghibli', file: 'invoke-03-ghibli.png' },
      { style: 'watercolor', file: 'invoke-04-watercolor.png' },
      { style: 'pixel_art', file: 'invoke-05-pixel_art.png' },
      { style: 'concept_art', file: 'invoke-06-concept_art.png' },
      { style: 'pastel', file: 'invoke-07-pastel.png' },
      { style: 'anime', file: 'invoke-08-anime.png' },
      { style: 'minimalist', file: 'invoke-09-minimalist.png' },
      { style: 'pop_art', file: 'invoke-10-pop_art.png' },
    ]
  },
  {
    id: 'pervasive',
    phrase: 'Pervasive',
    meaning: '만연한, 널리 퍼진',
    meaningEn: 'spreading throughout; widespread',
    example: 'The pervasive smell of smoke filled the building.',
    images: [
      { style: 'comic', file: 'pervasive-01-comic.png' },
      { style: 'watercolor', file: 'pervasive-02-watercolor.png' },
      { style: 'ghibli', file: 'pervasive-03-ghibli.png' },
      { style: 'disney', file: 'pervasive-04-disney.png' },
      { style: 'pop_art', file: 'pervasive-05-pop_art.png' },
      { style: 'minimalist', file: 'pervasive-06-minimalist.png' },
      { style: 'anime', file: 'pervasive-07-anime.png' },
      { style: 'concept_art', file: 'pervasive-08-concept_art.png' },
      { style: 'pastel', file: 'pervasive-09-pastel.png' },
      { style: 'pixel_art', file: 'pervasive-10-pixel_art.png' },
    ]
  },
];

// 이미지 URL 생성 헬퍼
export function getImageUrl(wordId: string, filename: string): string {
  return `${API_BASE_URL}/images/v3/${wordId}/${filename}`;
}

export type VocabWord = typeof vocabWords[number];
