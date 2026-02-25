#!/usr/bin/env python3
"""
meaning → meaning_kr 마이그레이션
다국어 확장 구조로 변환
"""
import json
from pathlib import Path

DATA_PATH = Path("/home/filadmin/word-shorts-app/data/phrasal-verbs.json")

def main():
    # 로드
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📚 총 {len(data)}개 항목 마이그레이션")
    
    # 변환
    for entry in data:
        if 'meaning' in entry:
            entry['meaning_kr'] = entry.pop('meaning')
            entry['meaning_en'] = ""  # 나중에 채울 수 있음
            entry['meaning_jp'] = ""  # 나중에 채울 수 있음
    
    # 저장
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 완료! 구조:")
    print(json.dumps(data[0], ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
