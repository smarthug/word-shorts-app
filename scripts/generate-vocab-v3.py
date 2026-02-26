#!/usr/bin/env python3
"""
단어별 이미지 생성 v3 - Two-step 방식
Step 1: 단어에 맞는 시나리오 자동 생성
Step 2: 시나리오별 이미지 프롬프트 생성
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
COMFYUI_URL = "http://localhost:8190"
OUTPUT_DIR = Path("/home/filadmin/Desktop/word-shorts-output/images/v3")
METADATA_DIR = Path("/home/filadmin/Desktop/word-shorts-output/metadata/v3")

client = OpenAI()

# 다양한 아트 스타일
STYLES = [
    {"id": "pastel", "name": "파스텔", "prompt": "soft pastel colors, gentle gradients, dreamy atmosphere, delicate and soothing aesthetic, light and airy feel"},
    {"id": "anime", "name": "애니메이션", "prompt": "anime style, vibrant colors, detailed linework, Japanese animation aesthetic"},
    {"id": "ghibli", "name": "지브리", "prompt": "Studio Ghibli style, soft watercolor textures, whimsical atmosphere, Hayao Miyazaki inspired"},
    {"id": "disney", "name": "디즈니/픽사", "prompt": "Disney Pixar 3D animation style, expressive characters, warm lighting, colorful"},
    {"id": "comic", "name": "만화", "prompt": "comic book style, bold outlines, dynamic composition, graphic novel aesthetic"},
    {"id": "watercolor", "name": "수채화", "prompt": "watercolor painting, soft edges, artistic brush strokes, traditional media look"},
    {"id": "minimalist", "name": "미니멀", "prompt": "minimalist illustration, simple geometric shapes, clean design, flat colors"},
    {"id": "pixel_art", "name": "픽셀아트", "prompt": "pixel art style, 16-bit retro game aesthetic, crisp pixels, vibrant colors, nostalgic gaming look"},
    {"id": "pop_art", "name": "팝아트", "prompt": "pop art style, bold colors, Ben-Day dots, Andy Warhol inspired, high contrast, comic book halftone"},
    {"id": "concept_art", "name": "컨셉아트", "prompt": "concept art style, digital painting, cinematic composition, professional illustration"}
]

def create_slug(word):
    slug = word.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug

def step1_generate_scenarios(word, meaning_en, meaning_kr, num_scenarios=10):
    """Step 1: 단어에 자연스러운 시나리오 생성"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "system",
                "content": """You are a vocabulary learning expert who creates memorable visual scenarios.

Your task: Generate diverse, realistic scenarios where a word would naturally be used.

Rules:
- Each scenario must be VISUALLY CONCRETE (can be depicted in an image)
- Each scenario must CLEARLY demonstrate the word's meaning
- Scenarios should be DIVERSE (different settings, people, situations)
- Focus on MEMORABLE scenes that help learners remember the word
- Output as JSON array with "scenario" (brief description) and "setting" (where it happens)
- Keep each scenario under 30 words"""
            }, {
                "role": "user",
                "content": f"""Word: {word}
English meaning: {meaning_en}
Korean meaning: {meaning_kr}

Generate {num_scenarios} diverse, visually concrete scenarios where "{word}" would naturally apply.

Output format:
[
  {{"scenario": "...", "setting": "..."}},
  ...
]"""
            }],
            temperature=0.9,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        raw_content = response.choices[0].message.content
        result = json.loads(raw_content)
        # Handle various response formats
        if isinstance(result, list):
            # Ensure each item is a dict
            scenarios = []
            for item in result[:num_scenarios]:
                if isinstance(item, dict):
                    scenarios.append(item)
                elif isinstance(item, str):
                    scenarios.append({"scenario": item, "setting": "various"})
            return scenarios
        elif isinstance(result, dict):
            if "scenarios" in result:
                return result["scenarios"][:num_scenarios]
            else:
                # Try to extract first list value
                for v in result.values():
                    if isinstance(v, list):
                        return v[:num_scenarios]
        return []
            
    except Exception as e:
        print(f"  ⚠️ 시나리오 생성 에러: {e}")
        return []

def step2_generate_image_prompt(word, meaning_en, scenario, setting, style):
    """Step 2: 시나리오 + 스타일을 이미지 프롬프트로 변환"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "system",
                "content": f"""You are an expert at creating image prompts for AI image generation.

Convert a scenario into a detailed, vivid image prompt in a SPECIFIC ART STYLE.

Rules:
- Output ONLY the image prompt, nothing else
- Make it visually specific and detailed
- IMPORTANT: Apply this art style throughout: {style['prompt']}
- Include composition hints (close-up, wide shot, etc.)
- Include emotional elements (expressions, body language)
- Always end with: anatomically correct, proper hand anatomy, no extra fingers, no text, no subtitles, no watermark
- Keep it under 100 words"""
            }, {
                "role": "user",
                "content": f"""Word: {word} ({meaning_en})
Scenario: {scenario}
Setting: {setting}
Art Style: {style['name']} - {style['prompt']}

Create a detailed image prompt in this specific art style."""
            }],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"  ⚠️ 프롬프트 생성 에러: {e}")
        return f"A scene showing {scenario} in {setting}, {style['prompt']}, no text, no watermark"

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
                "filename_prefix": "wordshorts-v3",
                "images": ["77:65", 0]
            },
            "class_type": "SaveImage",
            "_meta": {"title": "Save Image"}
        },
        "77:61": {
            "inputs": {"sampler_name": "euler"},
            "class_type": "KSamplerSelect"
        },
        "77:64": {
            "inputs": {
                "noise": ["77:73", 0],
                "guider": ["77:63", 0],
                "sampler": ["77:61", 0],
                "sigmas": ["77:62", 0],
                "latent_image": ["77:66", 0]
            },
            "class_type": "SamplerCustomAdvanced"
        },
        "77:65": {
            "inputs": {
                "samples": ["77:64", 0],
                "vae": ["77:72", 0]
            },
            "class_type": "VAEDecode"
        },
        "77:66": {
            "inputs": {
                "width": ["77:68", 0],
                "height": ["77:69", 0],
                "batch_size": 1
            },
            "class_type": "EmptyFlux2LatentImage"
        },
        "77:68": {"inputs": {"value": 1024}, "class_type": "PrimitiveInt"},  # Width
        "77:69": {"inputs": {"value": 1024}, "class_type": "PrimitiveInt"},  # Height (1:1 비율)
        "77:73": {"inputs": {"noise_seed": seed}, "class_type": "RandomNoise"},
        "77:70": {
            "inputs": {
                "unet_name": "flux-2-klein-4b.safetensors",
                "weight_dtype": "default"
            },
            "class_type": "UNETLoader"
        },
        "77:71": {
            "inputs": {
                "clip_name": "qwen_3_4b.safetensors",
                "type": "flux2",
                "device": "default"
            },
            "class_type": "CLIPLoader"
        },
        "77:72": {
            "inputs": {"vae_name": "flux2-vae.safetensors"},
            "class_type": "VAELoader"
        },
        "77:63": {
            "inputs": {
                "cfg": 1,
                "model": ["77:70", 0],
                "positive": ["77:74", 0],
                "negative": ["77:76", 0]
            },
            "class_type": "CFGGuider"
        },
        "77:76": {
            "inputs": {"conditioning": ["77:74", 0]},
            "class_type": "ConditioningZeroOut"
        },
        "77:74": {
            "inputs": {
                "text": ["76", 0],
                "clip": ["77:71", 0]
            },
            "class_type": "CLIPTextEncode"
        },
        "77:62": {
            "inputs": {
                "steps": 4,
                "width": ["77:68", 0],
                "height": ["77:69", 0]
            },
            "class_type": "Flux2Scheduler"
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

def process_word(word, meaning_en, meaning_kr, images_per_word=10):
    """단어 처리 (Two-step)"""
    slug = create_slug(word)
    
    word_output_dir = OUTPUT_DIR / slug
    word_output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"📝 {word}")
    print(f"   EN: {meaning_en}")
    print(f"   KR: {meaning_kr}")
    print(f"{'='*60}")
    
    # Step 1: 시나리오 생성
    print(f"\n🎬 Step 1: 시나리오 생성 중...")
    scenarios = step1_generate_scenarios(word, meaning_en, meaning_kr, images_per_word)
    
    if not scenarios:
        print("  ❌ 시나리오 생성 실패")
        return None
    
    print(f"  ✅ {len(scenarios)}개 시나리오 생성됨:")
    for i, s in enumerate(scenarios, 1):
        print(f"     {i}. [{s.get('setting', 'N/A')}] {s.get('scenario', 'N/A')[:50]}...")
    
    # Step 2: 이미지 생성 (시나리오 × 스타일)
    print(f"\n🖼️  Step 2: 이미지 생성 중...")
    print(f"   🎨 스타일: {len(STYLES)}가지")
    
    word_results = []
    
    # 스타일을 셔플해서 다양하게 적용
    shuffled_styles = STYLES.copy()
    random.shuffle(shuffled_styles)
    
    for i, scenario_data in enumerate(scenarios, 1):
        scenario = scenario_data.get("scenario", "")
        setting = scenario_data.get("setting", "")
        
        # 각 시나리오마다 다른 스타일 적용
        style = shuffled_styles[(i - 1) % len(shuffled_styles)]
        
        output_path = word_output_dir / f"{slug}-{i:02d}-{style['id']}.png"
        
        if output_path.exists():
            print(f"  [{i}/{len(scenarios)}] 이미 존재, 스킵")
            continue
        
        print(f"  [{i}/{len(scenarios)}] 🎬 {setting[:15]}... | 🎨 {style['name']}")
        
        # 이미지 프롬프트 생성 (스타일 포함)
        image_prompt = step2_generate_image_prompt(word, meaning_en, scenario, setting, style)
        print(f"    → {image_prompt[:50]}...")
        
        # ComfyUI로 생성
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
                "variation": i,
                "scenario": scenario,
                "setting": setting,
                "style_id": style["id"],
                "style_name": style["name"],
                "prompt": image_prompt,
                "seed": seed,
                "path": str(output_path)
            })
    
    # 메타데이터 저장
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    
    metadata = {
        "word": word,
        "slug": slug,
        "meaning_en": meaning_en,
        "meaning_kr": meaning_kr,
        "version": "v3",
        "resolution": "1024x1024",
        "scenarios_generated": scenarios,
        "images": word_results,
        "model": "flux-2-klein-4b",
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    meta_path = METADATA_DIR / f"{slug}.json"
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 메타데이터: {meta_path}")
    return metadata

def main():
    # 환경변수 또는 기본값
    words_input = os.environ.get('WORDS', 'Replenish')
    images_per_word = int(os.environ.get('IMAGES_PER_WORD', 10))
    
    # 테스트 데이터 (예문 포함)
    WORD_DATA = {
        "Replenish": {
            "en": "to fill or supply again",
            "kr": "보충하다, 다시 채우다",
            "example": "We need to replenish our stock before the holiday rush."
        },
        "Instigate": {
            "en": "to cause or encourage to happen",
            "kr": "선동하다, 부추기다",
            "example": "He was accused of instigating the riot."
        },
        "Substantiate": {
            "en": "to provide evidence to prove",
            "kr": "입증하다, 실증하다",
            "example": "Can you substantiate your claims with evidence?"
        },
        "Deliberate": {
            "en": "done intentionally; to think carefully",
            "kr": "신중한, 고의적인; 숙고하다",
            "example": "The jury will deliberate before reaching a verdict."
        },
        "Strenuous": {
            "en": "requiring great effort or energy",
            "kr": "격렬한, 힘든",
            "example": "The strenuous hike left everyone exhausted."
        },
        "Conjunction": {
            "en": "a combination; connecting word",
            "kr": "결합, 접속사",
            "example": "The event was held in conjunction with the annual festival."
        },
        "Extant": {
            "en": "still existing; not destroyed",
            "kr": "현존하는, 남아있는",
            "example": "Only a few copies of the manuscript are still extant."
        },
        "Sedentary": {
            "en": "involving much sitting; inactive",
            "kr": "앉아서 하는, 주로 앉아 있는",
            "example": "A sedentary lifestyle can lead to health problems."
        },
        "Invoke": {
            "en": "to call upon; to cite as authority",
            "kr": "호출하다, 발동하다",
            "example": "The lawyer invoked the Fifth Amendment."
        },
        "Pervasive": {
            "en": "spreading throughout; widespread",
            "kr": "만연한, 널리 퍼진",
            "example": "The pervasive smell of smoke filled the building."
        },
    }
    
    words = [w.strip() for w in words_input.split(',')]
    
    print("=" * 60)
    print("🎨 Word Shorts 이미지 생성 v3 (Two-step)")
    print("=" * 60)
    print(f"📚 단어: {words}")
    print(f"🖼️  단어당 이미지: {images_per_word}개")
    print("=" * 60)
    
    all_results = []
    
    for word in words:
        word = word.strip()
        if word in WORD_DATA:
            meaning_en = WORD_DATA[word]["en"]
            meaning_kr = WORD_DATA[word]["kr"]
        else:
            meaning_en = ""
            meaning_kr = ""
        
        result = process_word(word, meaning_en, meaning_kr, images_per_word)
        if result:
            all_results.append(result)
    
    print("\n" + "=" * 60)
    print("✅ 완료!")
    print(f"📁 출력: {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
