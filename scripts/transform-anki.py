#!/usr/bin/env python3
"""
Anki JSON → Word Shorts KV 형식으로 변환
"""
import json
import re
from pathlib import Path

def clean_text(text):
    """텍스트 정리"""
    if not text:
        return ""
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)
    # &nbsp; 제거
    text = text.replace('&nbsp;', ' ')
    # 따옴표 정리
    text = text.strip().strip('"\'')
    # 여러 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_phrasal_verb(front):
    """숙어 추출 (번호 제거)"""
    # "back up¹" → "back up"
    clean = re.sub(r'[¹²³⁴⁵⁶⁷⁸⁹⁰]', '', front)
    return clean.strip()

def create_slug(phrase):
    """URL-safe slug 생성"""
    slug = phrase.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug

def transform_entry(entry):
    """Anki 엔트리 → KV 형식"""
    fields = entry.get('fieldsMap', {})
    
    phrase = clean_text(fields.get('Front', ''))
    base_phrase = extract_phrasal_verb(phrase)
    meaning = clean_text(fields.get('뜻', ''))
    example = clean_text(fields.get('예문', ''))
    
    # 예문에서 빈칸 복원
    if example and base_phrase:
        parts = base_phrase.split()
        if len(parts) >= 2:
            # "__ __" 패턴 찾아서 대체
            example_filled = example
            # 다양한 빈칸 패턴 처리
            example_filled = re.sub(r'__\s*__', f'{parts[0]} {parts[1]}', example_filled)
            example_filled = re.sub(r'__ing\s*__', f'{parts[0]}ing {parts[1]}', example_filled)
            example_filled = re.sub(r'__ed\s*__', f'{parts[0]}ed {parts[1]}', example_filled)
            example_filled = re.sub(r'__s\s*__', f'{parts[0]}s {parts[1]}', example_filled)
    else:
        example_filled = example
    
    return {
        "id": create_slug(phrase),
        "phrase": phrase,
        "basePhrase": base_phrase,
        "meaning": meaning,
        "example": example_filled,
        "exampleOriginal": example,
        "noteId": entry.get('noteId'),
        "assets": []  # 나중에 이미지/영상 추가
    }

def main():
    input_path = Path('/home/filadmin/.openclaw/media/inbound/file_2---8a7f2e5a-a6f5-47d5-91ac-3d775722e76d.json')
    output_path = Path('/home/filadmin/word-shorts-app/data/phrasal-verbs.json')
    
    with open(input_path, 'r', encoding='utf-8') as f:
        anki_data = json.load(f)
    
    transformed = []
    seen_ids = set()
    
    for entry in anki_data:
        item = transform_entry(entry)
        
        # 중복 ID 처리
        original_id = item['id']
        counter = 1
        while item['id'] in seen_ids:
            item['id'] = f"{original_id}-{counter}"
            counter += 1
        seen_ids.add(item['id'])
        
        if item['phrase'] and item['meaning']:
            transformed.append(item)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(transformed, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 변환 완료: {len(transformed)}개 항목")
    print(f"📁 저장: {output_path}")
    
    # 샘플 출력
    print("\n📝 샘플 (처음 3개):")
    for item in transformed[:3]:
        print(f"  - {item['phrase']}: {item['meaning']}")
        print(f"    예문: {item['example'][:50]}...")

if __name__ == '__main__':
    main()
