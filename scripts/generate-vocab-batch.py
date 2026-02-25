#!/usr/bin/env python3
"""
단어별 10개 이미지 배치 생성
Flux 2 Klein + GPT-4o-mini
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

# 오늘 생성할 단어들
WORDS = [
    {"word": "Replenish", "meaning_kr": "보충하다, 다시 채우다"},
    {"word": "Instigate", "meaning_kr": "선동하다, 부추기다"},
    {"word": "Substantiate", "meaning_kr": "입증하다, 실증하다"},
    {"word": "Deliberate", "meaning_kr": "신중한, 고의적인; 숙고하다"},
    {"word": "Strenuous", "meaning_kr": "격렬한, 힘든"},
    {"word": "Conjunction", "meaning_kr": "결합, 접속사"},
    {"word": "Extant", "meaning_kr": "현존하는, 남아있는"},
    {"word": "Sedentary", "meaning_kr": "앉아서 하는, 주로 앉아 있는"},
    {"word": "Invoke", "meaning_kr": "호출하다, 발동하다"},
    {"word": "Pervasive", "meaning_kr": "만연한, 널리 퍼진"},
]

def create_slug(word):
    slug = word.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug

def generate_image_prompt(word, meaning_kr, variation_num):
    """GPT로 이미지 프롬프트 생성 (variation마다 다르게)"""
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
- Include: shallow depth of field, natural expressions (if people involved)
- Always end with: no text, no subtitles, no watermark
- Keep it under 100 words
- Each prompt should show a DIFFERENT scenario/scene for the same word
- Be creative and diverse in your scenes"""
            }, {
                "role": "user",
                "content": f"Word: {word}\nMeaning: {meaning_kr}\nVariation: {variation_num}/10 (make this scene unique from others)"
            }],
            temperature=0.9,  # 높은 temperature로 다양성 확보
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"  ⚠️ GPT 에러: {e}")
        return f"A visual scene representing '{word}', cinematic realism, natural lighting, no text, no subtitles"

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

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    
    images_per_word = int(os.environ.get('IMAGES_PER_WORD', 10))
    total_words = len(WORDS)
    total_images = total_words * images_per_word
    
    print(f"📚 단어: {total_words}개")
    print(f"🖼️  단어당 이미지: {images_per_word}개")
    print(f"📊 총 이미지: {total_images}개")
    print(f"🎨 모델: Flux 2 Klein (4 steps)")
    print("=" * 60)
    
    all_results = []
    image_count = 0
    
    for word_idx, word_entry in enumerate(WORDS, 1):
        word = word_entry["word"]
        meaning_kr = word_entry["meaning_kr"]
        slug = create_slug(word)
        
        print(f"\n[{word_idx}/{total_words}] 📝 {word} ({meaning_kr})")
        print("-" * 40)
        
        word_results = []
        
        for var_num in range(1, images_per_word + 1):
            image_count += 1
            output_path = OUTPUT_DIR / f"{slug}-{var_num:02d}.png"
            
            # 이미 존재하면 스킵
            if output_path.exists():
                print(f"  [{var_num}/{images_per_word}] 이미 존재, 스킵")
                continue
            
            print(f"  [{var_num}/{images_per_word}] 프롬프트 생성...")
            image_prompt = generate_image_prompt(word, meaning_kr, var_num)
            print(f"    → {image_prompt[:50]}...")
            
            print(f"  [{var_num}/{images_per_word}] 이미지 생성...")
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
                    "prompt": image_prompt,
                    "seed": seed,
                    "path": str(output_path)
                })
        
        # 단어별 메타데이터 저장
        metadata = {
            "word": word,
            "slug": slug,
            "meaning_kr": meaning_kr,
            "meaning_en": "",
            "meaning_jp": "",
            "images": word_results,
            "model": "flux-2-klein-4b",
            "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        
        meta_path = METADATA_DIR / f"{slug}.json"
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        all_results.append(metadata)
        print(f"  📄 메타데이터: {meta_path.name}")
    
    # 전체 결과 저장
    results_path = OUTPUT_DIR / "batch-results.json"
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"✅ 완료!")
    print(f"📁 이미지: {OUTPUT_DIR}")
    print(f"📄 결과: {results_path}")

if __name__ == '__main__':
    main()
