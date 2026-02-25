#!/usr/bin/env python3
"""
단어별 이미지 생성 v2 - 다양한 컨텍스트 강제 적용
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

client = OpenAI()

# 다양한 컨텍스트 카테고리
CONTEXTS = [
    {
        "id": "workplace",
        "name": "직장/비즈니스",
        "hint": "office, business meeting, corporate environment, professional setting"
    },
    {
        "id": "home",
        "name": "가정/일상",
        "hint": "home, living room, kitchen, family life, domestic setting"
    },
    {
        "id": "nature",
        "name": "자연/야외",
        "hint": "outdoors, nature, park, forest, beach, mountains"
    },
    {
        "id": "urban",
        "name": "도시/거리",
        "hint": "city street, urban environment, cafe, restaurant, public space"
    },
    {
        "id": "education",
        "name": "학교/교육",
        "hint": "classroom, school, university, library, studying"
    },
    {
        "id": "technology",
        "name": "기술/디지털",
        "hint": "computer, smartphone, technology, digital world, modern devices"
    },
    {
        "id": "sports",
        "name": "스포츠/운동",
        "hint": "gym, sports field, exercise, athletic activity, fitness"
    },
    {
        "id": "medical",
        "name": "의료/건강",
        "hint": "hospital, doctor, health, medical care, wellness"
    },
    {
        "id": "social",
        "name": "사교/관계",
        "hint": "friends gathering, party, social event, relationships, conversation"
    },
    {
        "id": "travel",
        "name": "여행/이동",
        "hint": "airport, train station, travel, journey, adventure"
    }
]

# 다양한 구도/앵글
COMPOSITIONS = [
    "wide establishing shot showing the full scene",
    "medium shot focusing on 1-2 people",
    "close-up shot emphasizing details and expressions",
    "over-the-shoulder perspective",
    "bird's eye view from above",
    "low angle shot looking up",
    "profile view from the side",
    "environmental portrait with context",
    "candid documentary style capture",
    "dramatic lighting with shadows"
]

def create_slug(word):
    slug = word.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug

def generate_image_prompt_v2(word, meaning_en, meaning_kr, context, composition, variation_num):
    """개선된 프롬프트 생성 - 컨텍스트와 구도 강제 적용"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": """You are an expert at creating visual prompts for AI image generation that help people learn vocabulary.

Your goal: Create a scene that CLEARLY illustrates the word's meaning in a MEMORABLE way.

Rules:
- Output ONLY the image prompt, nothing else
- The scene must use the SPECIFIED CONTEXT (setting/environment)
- The scene must use the SPECIFIED COMPOSITION (camera angle/framing)
- Show the CORE MEANING of the word through action/situation (not just objects)
- If possible, show a BEFORE→AFTER or CAUSE→EFFECT dynamic
- Make it emotionally engaging and memorable
- Style: cinematic realism, natural lighting
- Always end with: no text, no subtitles, no watermark
- Keep it under 100 words"""
            }, {
                "role": "user",
                "content": f"""Word: {word}
English meaning: {meaning_en}
Korean meaning: {meaning_kr}

REQUIRED CONTEXT: {context['name']} ({context['hint']})
REQUIRED COMPOSITION: {composition}

Create a unique scene that clearly shows the meaning of "{word}" in this specific context and composition."""
            }],
            temperature=0.85,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"  ⚠️ GPT 에러: {e}")
        return f"A scene showing '{word}' ({meaning_en}) in {context['hint']}, {composition}, cinematic realism, no text, no watermark"

def get_flux2_workflow(prompt, seed=None):
    """Flux 2 Klein 워크플로우"""
    if seed is None:
        seed = random.randint(0, 2**53 - 1)
    
    return {
        "76": {
            "inputs": {"value": prompt},
            "class_type": "PrimitiveStringMultiline",
            "_meta": {"title": "Prompt"}
        },
        "78": {
            "inputs": {
                "filename_prefix": "wordshorts-v2",
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
    }, seed

def queue_prompt(workflow):
    data = {"prompt": workflow}
    response = requests.post(f"{COMFYUI_URL}/prompt", json=data)
    return response.json()

def wait_for_completion(prompt_id, timeout=120):
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
    url = f"{COMFYUI_URL}/view?filename={filename}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

def process_word(word_entry, images_per_word=10):
    """단어 하나 처리"""
    word = word_entry["word"]
    meaning_kr = word_entry.get("meaning_kr", "")
    meaning_en = word_entry.get("meaning_en", "")
    slug = create_slug(word)
    
    # v2 출력 디렉토리
    word_output_dir = OUTPUT_DIR / "v2" / slug
    word_output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📝 {word}")
    print(f"   EN: {meaning_en}")
    print(f"   KR: {meaning_kr}")
    print("-" * 50)
    
    word_results = []
    
    # 컨텍스트와 구도를 섞어서 사용
    shuffled_contexts = random.sample(CONTEXTS, min(images_per_word, len(CONTEXTS)))
    shuffled_compositions = random.sample(COMPOSITIONS, min(images_per_word, len(COMPOSITIONS)))
    
    for var_num in range(1, images_per_word + 1):
        context = shuffled_contexts[(var_num - 1) % len(shuffled_contexts)]
        composition = shuffled_compositions[(var_num - 1) % len(shuffled_compositions)]
        
        output_path = word_output_dir / f"{slug}-{var_num:02d}.png"
        
        # 이미 존재하면 스킵
        if output_path.exists():
            print(f"  [{var_num}/{images_per_word}] 이미 존재, 스킵")
            continue
        
        print(f"  [{var_num}/{images_per_word}] 🎬 {context['id']} + {composition[:20]}...")
        
        # 프롬프트 생성
        image_prompt = generate_image_prompt_v2(
            word, meaning_en, meaning_kr, context, composition, var_num
        )
        print(f"    → {image_prompt[:60]}...")
        
        # 이미지 생성
        workflow, seed = get_flux2_workflow(image_prompt)
        result = queue_prompt(workflow)
        prompt_id = result.get("prompt_id")
        
        if not prompt_id:
            print(f"    ❌ 큐잉 실패")
            continue
        
        history = wait_for_completion(prompt_id)
        if not history:
            print(f"    ❌ 타임아웃")
            continue
        
        filename = get_generated_image(history)
        if not filename:
            print(f"    ❌ 이미지 없음")
            continue
        
        if download_image(filename, output_path):
            print(f"    ✅ {output_path.name}")
            
            word_results.append({
                "variation": var_num,
                "context": context["id"],
                "context_name": context["name"],
                "composition": composition,
                "prompt": image_prompt,
                "seed": seed,
                "path": str(output_path)
            })
    
    # 메타데이터 저장
    metadata = {
        "word": word,
        "slug": slug,
        "meaning_kr": meaning_kr,
        "meaning_en": meaning_en,
        "meaning_jp": word_entry.get("meaning_jp", ""),
        "version": "v2",
        "images": word_results,
        "model": "flux-2-klein-4b",
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    meta_dir = METADATA_DIR / "v2"
    meta_dir.mkdir(parents=True, exist_ok=True)
    meta_path = meta_dir / f"{slug}.json"
    
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"  📄 메타: {meta_path.name}")
    return metadata

def main():
    # 테스트 단어 (환경변수 또는 기본값)
    test_words = os.environ.get('WORDS', 'Replenish').split(',')
    images_per_word = int(os.environ.get('IMAGES_PER_WORD', 10))
    
    words_data = []
    for w in test_words:
        w = w.strip()
        words_data.append({
            "word": w,
            "meaning_kr": "",  # 필요시 채움
            "meaning_en": ""
        })
    
    # 하드코딩된 테스트 데이터 (Replenish)
    if test_words == ['Replenish']:
        words_data = [{
            "word": "Replenish",
            "meaning_kr": "보충하다, 다시 채우다",
            "meaning_en": "to fill or supply again"
        }]
    
    print("=" * 60)
    print("🎨 Word Shorts 이미지 생성 v2")
    print("=" * 60)
    print(f"📚 단어: {[w['word'] for w in words_data]}")
    print(f"🖼️  단어당 이미지: {images_per_word}개")
    print(f"🎯 컨텍스트: {len(CONTEXTS)}가지")
    print(f"📐 구도: {len(COMPOSITIONS)}가지")
    print("=" * 60)
    
    all_results = []
    
    for word_entry in words_data:
        result = process_word(word_entry, images_per_word)
        if result:
            all_results.append(result)
    
    print("\n" + "=" * 60)
    print("✅ 완료!")
    print(f"📁 출력: {OUTPUT_DIR}/v2/")

if __name__ == '__main__':
    main()
