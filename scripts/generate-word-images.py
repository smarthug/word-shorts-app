#!/usr/bin/env python3
"""
단어 → 이미지 생성 파이프라인
ComfyUI + Flux 2 Klein으로 단어에 맞는 이미지 생성
"""
import json
import requests
import time
import os
import re
import random
from pathlib import Path
from openai import OpenAI

# 설정
COMFYUI_URL = "http://localhost:8188"
OUTPUT_DIR = Path("/home/filadmin/Desktop/word-shorts-output/images")
METADATA_DIR = Path("/home/filadmin/Desktop/word-shorts-output/metadata")
DATA_PATH = Path("/home/filadmin/word-shorts-app/data/phrasal-verbs.json")

# OpenAI 클라이언트
client = OpenAI()

def clean_text(text):
    """텍스트 정리"""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&nbsp;', ' ')
    text = re.sub(r'\[sound:[^\]]+\]', '', text)
    return text.strip()

def create_slug(word):
    """파일명용 슬러그"""
    slug = word.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug

def generate_image_prompt(word, meaning, example):
    """GPT로 이미지 프롬프트 생성"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": """You are an expert at creating visual prompts for AI image generation.
Given an English vocabulary word, create a vivid, concrete scene that illustrates its meaning.

Rules:
- Output ONLY the image prompt, nothing else
- Make it visually concrete and memorable  
- Style: cinematic realism, natural lighting, documentary style photography
- Include: shallow depth of field, natural human micro-expressions (if people involved)
- Always end with: no text, no subtitles, no watermark
- Keep it under 100 words
- Focus on a single clear scene that captures the word's meaning"""
            }, {
                "role": "user",
                "content": f"Word: {word}\nMeaning: {meaning}\nExample: {example}"
            }],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"  ⚠️ GPT 에러: {e}")
        return f"A visual scene representing '{word}' meaning '{meaning}', cinematic realism, natural lighting, no text, no subtitles"

def get_flux2_workflow(prompt, seed=None):
    """Flux 2 Klein 워크플로우 생성"""
    if seed is None:
        seed = random.randint(0, 2**53 - 1)
    
    return {
        "76": {
            "inputs": {
                "value": prompt
            },
            "class_type": "PrimitiveStringMultiline",
            "_meta": {"title": "Prompt"}
        },
        "78": {
            "inputs": {
                "filename_prefix": "wordshorts",
                "images": ["77:65", 0]
            },
            "class_type": "SaveImage",
            "_meta": {"title": "Save Image"}
        },
        "77:61": {
            "inputs": {"sampler_name": "euler"},
            "class_type": "KSamplerSelect",
            "_meta": {"title": "KSamplerSelect"}
        },
        "77:64": {
            "inputs": {
                "noise": ["77:73", 0],
                "guider": ["77:63", 0],
                "sampler": ["77:61", 0],
                "sigmas": ["77:62", 0],
                "latent_image": ["77:66", 0]
            },
            "class_type": "SamplerCustomAdvanced",
            "_meta": {"title": "SamplerCustomAdvanced"}
        },
        "77:65": {
            "inputs": {
                "samples": ["77:64", 0],
                "vae": ["77:72", 0]
            },
            "class_type": "VAEDecode",
            "_meta": {"title": "VAE Decode"}
        },
        "77:66": {
            "inputs": {
                "width": ["77:68", 0],
                "height": ["77:69", 0],
                "batch_size": 1
            },
            "class_type": "EmptyFlux2LatentImage",
            "_meta": {"title": "Empty Flux 2 Latent"}
        },
        "77:68": {
            "inputs": {"value": 1024},
            "class_type": "PrimitiveInt",
            "_meta": {"title": "Width"}
        },
        "77:69": {
            "inputs": {"value": 1024},
            "class_type": "PrimitiveInt",
            "_meta": {"title": "Height"}
        },
        "77:73": {
            "inputs": {"noise_seed": seed},
            "class_type": "RandomNoise",
            "_meta": {"title": "RandomNoise"}
        },
        "77:70": {
            "inputs": {
                "unet_name": "flux-2-klein-4b.safetensors",
                "weight_dtype": "default"
            },
            "class_type": "UNETLoader",
            "_meta": {"title": "Load Diffusion Model"}
        },
        "77:71": {
            "inputs": {
                "clip_name": "qwen_3_4b.safetensors",
                "type": "flux2",
                "device": "default"
            },
            "class_type": "CLIPLoader",
            "_meta": {"title": "Load CLIP"}
        },
        "77:72": {
            "inputs": {"vae_name": "flux2-vae.safetensors"},
            "class_type": "VAELoader",
            "_meta": {"title": "Load VAE"}
        },
        "77:63": {
            "inputs": {
                "cfg": 1,
                "model": ["77:70", 0],
                "positive": ["77:74", 0],
                "negative": ["77:76", 0]
            },
            "class_type": "CFGGuider",
            "_meta": {"title": "CFGGuider"}
        },
        "77:76": {
            "inputs": {"conditioning": ["77:74", 0]},
            "class_type": "ConditioningZeroOut",
            "_meta": {"title": "ConditioningZeroOut"}
        },
        "77:74": {
            "inputs": {
                "text": ["76", 0],
                "clip": ["77:71", 0]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "CLIP Text Encode (Positive Prompt)"}
        },
        "77:62": {
            "inputs": {
                "steps": 4,
                "width": ["77:68", 0],
                "height": ["77:69", 0]
            },
            "class_type": "Flux2Scheduler",
            "_meta": {"title": "Flux2Scheduler"}
        }
    }

def queue_prompt(workflow):
    """ComfyUI에 프롬프트 큐잉"""
    data = {"prompt": workflow}
    response = requests.post(f"{COMFYUI_URL}/prompt", json=data)
    return response.json()

def wait_for_completion(prompt_id, timeout=120):
    """이미지 생성 완료 대기"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(f"{COMFYUI_URL}/history/{prompt_id}")
            history = response.json()
            if prompt_id in history:
                return history[prompt_id]
        except:
            pass
        time.sleep(1)
    return None

def get_generated_image(history):
    """생성된 이미지 경로 가져오기"""
    try:
        outputs = history.get("outputs", {})
        for node_id, output in outputs.items():
            if "images" in output:
                for img in output["images"]:
                    return img.get("filename")
    except:
        pass
    return None

def download_image(filename, save_path):
    """ComfyUI에서 이미지 다운로드"""
    url = f"{COMFYUI_URL}/view?filename={filename}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

def save_metadata(slug, metadata):
    """메타데이터 저장 (KV 업로드 전 로컬 백업)"""
    meta_path = METADATA_DIR / f"{slug}.json"
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    return meta_path

def process_word(entry, index, total):
    """단어 하나 처리"""
    word = clean_text(entry.get('phrase', ''))  # phrasal-verbs.json 구조
    meaning_kr = clean_text(entry.get('meaning_kr', ''))
    meaning_en = clean_text(entry.get('meaning_en', ''))
    example = clean_text(entry.get('example', ''))
    
    if not word or not meaning_kr:
        return None
    
    slug = create_slug(word)
    output_path = OUTPUT_DIR / f"{slug}.png"
    
    # 이미 존재하면 스킵
    if output_path.exists():
        print(f"[{index}/{total}] {word} - 이미 존재, 스킵")
        return {"word": word, "path": str(output_path), "skipped": True}
    
    print(f"[{index}/{total}] {word} ({meaning_kr})")
    
    # 1. 이미지 프롬프트 생성 (영어 뜻 있으면 영어로, 없으면 한국어로)
    meaning_for_prompt = meaning_en if meaning_en else meaning_kr
    print(f"  → 프롬프트 생성 중...")
    image_prompt = generate_image_prompt(word, meaning_for_prompt, example)
    print(f"  → 프롬프트: {image_prompt[:60]}...")
    
    # 2. 시드 생성
    seed = random.randint(0, 2**53 - 1)
    
    # 3. ComfyUI로 이미지 생성
    print(f"  → 이미지 생성 중 (Flux 2 Klein)...")
    workflow = get_flux2_workflow(image_prompt, seed)
    result = queue_prompt(workflow)
    prompt_id = result.get("prompt_id")
    
    if not prompt_id:
        print(f"  ❌ 큐잉 실패: {result}")
        return None
    
    # 4. 완료 대기
    history = wait_for_completion(prompt_id)
    if not history:
        print(f"  ❌ 타임아웃")
        return None
    
    # 5. 이미지 다운로드
    filename = get_generated_image(history)
    if not filename:
        print(f"  ❌ 이미지 없음")
        return None
    
    if download_image(filename, output_path):
        print(f"  ✅ 저장: {output_path}")
        
        # 6. 메타데이터 저장
        meaning_jp = clean_text(entry.get('meaning_jp', ''))
        metadata = {
            "word": word,
            "slug": slug,
            "meaning_kr": meaning_kr,
            "meaning_en": meaning_en,
            "meaning_jp": meaning_jp,
            "example": example,
            "image": {
                "prompt": image_prompt,
                "model": "flux-2-klein-4b",
                "seed": seed,
                "steps": 4,
                "cfg": 1,
                "width": 1024,
                "height": 1024,
                "sampler": "euler",
                "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            },
            "promptGeneration": {
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
        }
        meta_path = save_metadata(slug, metadata)
        print(f"  📄 메타: {meta_path}")
        
        return {
            "word": word,
            "meaning_kr": meaning_kr,
            "prompt": image_prompt,
            "path": str(output_path),
            "slug": slug,
            "seed": seed
        }
    
    return None

def main():
    # 출력 디렉토리 확인
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 데이터 로드
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📚 총 {len(data)}개 단어")
    print(f"📁 이미지 출력: {OUTPUT_DIR}")
    print(f"📄 메타데이터: {METADATA_DIR}")
    print(f"🎨 모델: Flux 2 Klein (4 steps)")
    print("-" * 50)
    
    # 결과 저장용
    results = []
    
    # 처리 (LIMIT 환경변수로 제한)
    limit = int(os.environ.get('LIMIT', 10))
    print(f"🎯 처리할 단어: {limit}개")
    print("-" * 50)
    
    for i, entry in enumerate(data[:limit], 1):
        result = process_word(entry, i, min(limit, len(data)))
        if result:
            results.append(result)
        time.sleep(0.5)  # API 레이트 리밋
    
    # 전체 결과 저장
    results_path = OUTPUT_DIR / "results.json"
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("-" * 50)
    print(f"✅ 완료: {len(results)}개 이미지 생성")
    print(f"📄 결과: {results_path}")

if __name__ == '__main__':
    main()
