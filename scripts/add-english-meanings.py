#!/usr/bin/env python3
"""
meaning_kr → meaning_en 번역
GPT-4o-mini로 영어 뜻 추가
"""
import json
import time
from pathlib import Path
from openai import OpenAI

DATA_PATH = Path("/home/filadmin/word-shorts-app/data/phrasal-verbs.json")
client = OpenAI()

def translate_to_english(phrase, meaning_kr):
    """한국어 뜻을 영어로 번역"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": """You are a dictionary expert. Given an English phrasal verb and its Korean meaning, provide a concise English definition.

Rules:
- Output ONLY the English definition, nothing else
- Keep it short and clear (under 10 words if possible)
- Use the infinitive form (e.g., "to explain", "to account")
- Match the style of dictionary definitions"""
            }, {
                "role": "user",
                "content": f"Phrasal verb: {phrase}\nKorean meaning: {meaning_kr}"
            }],
            temperature=0.3,
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"  ⚠️ 에러: {e}")
        return ""

def main():
    # 로드
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total = len(data)
    print(f"📚 총 {total}개 항목")
    print(f"💰 예상 비용: ~$0.05")
    print("-" * 50)
    
    # 이미 meaning_en이 있는 것은 스킵
    to_process = [e for e in data if not e.get('meaning_en')]
    print(f"🎯 번역할 항목: {len(to_process)}개")
    print("-" * 50)
    
    processed = 0
    for i, entry in enumerate(data):
        if entry.get('meaning_en'):
            continue
        
        phrase = entry.get('phrase', '')
        meaning_kr = entry.get('meaning_kr', '')
        
        if not phrase or not meaning_kr:
            continue
        
        processed += 1
        if processed % 100 == 1:
            print(f"[{processed}/{len(to_process)}] {phrase} ({meaning_kr})")
        
        meaning_en = translate_to_english(phrase, meaning_kr)
        entry['meaning_en'] = meaning_en
        
        # 레이트 리밋 방지
        if processed % 50 == 0:
            time.sleep(1)
            # 중간 저장
            with open(DATA_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  💾 중간 저장 ({processed}개 완료)")
    
    # 최종 저장
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("-" * 50)
    print(f"✅ 완료! {processed}개 번역")
    
    # 샘플 출력
    print("\n📝 샘플:")
    for entry in data[:5]:
        print(f"  {entry['phrase']}: {entry['meaning_kr']} → {entry['meaning_en']}")

if __name__ == '__main__':
    main()
