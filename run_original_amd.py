import os
# Force ROCm AMD environment by hiding NVIDIA and showing AMD GPU
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["ROCR_VISIBLE_DEVICES"] = "0"
os.environ["PYTORCH_ALLOC_CONF"] = "expandable_segments:True"

import av
import json
import numpy as np
import torch
from transformers import LlavaNextVideoForConditionalGeneration, LlavaNextVideoProcessor

def extract_frames(video_path, num_frames=8):
    """
    Extracts a fixed number of frames from a video file safely.
    """
    print(f"📹 Opening video file: {video_path}")
    container = av.open(video_path)
    video_stream = container.streams.video[0]
    total_frames = video_stream.frames
    
    # Safe fallback if total_frames metadata is missing
    if total_frames is None or total_frames <= 0:
        duration = video_stream.duration
        time_base = video_stream.time_base
        avg_frame_rate = video_stream.average_rate
        if duration and time_base and avg_frame_rate:
            total_seconds = float(duration * time_base)
            total_frames = int(total_seconds * float(avg_frame_rate))
        else:
            total_frames = 100
            
    print(f"🎞️  Total frames (est): {total_frames}")
    
    indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
    print(f"🎯 Sampling frame indices: {list(indices)}")
    
    frames = []
    current_idx = 0
    sampled_count = 0
    
    for frame in container.decode(video=0):
        if current_idx in indices:
            # Convert PyAV frame to PIL Image, resize to 512x288 to optimize VRAM
            img = frame.to_image().resize((512, 288))
            frames.append(np.array(img))
            sampled_count += 1
            if sampled_count >= num_frames:
                break
        current_idx += 1
        
    container.close()
    print(f"✅ Extracted {len(frames)} frames. Shape of one frame: {frames[0].shape}")
    return np.stack(frames)

def main():
    model_id = "llava-hf/LLaVA-NeXT-Video-7B-hf"
    
    # Verify device
    print("🖥️  PyTorch GPU backend check:")
    print(f"   CUDA (ROCm) available: {torch.cuda.is_available()}")
    print(f"   Device count: {torch.cuda.device_count()}")
    if torch.cuda.is_available():
        print(f"   Device Name: {torch.cuda.get_device_name(0)}")
        device = "cuda:0"
    else:
        print("   ⚠️ No GPU detected by PyTorch ROCm. Falling back to CPU!")
        device = "cpu"
        
    # Load model completely on GPU (no CPU offloading)
    print(f"📥 Loading original LLaVA model: {model_id} on {device}...")
    model = LlavaNextVideoForConditionalGeneration.from_pretrained(
        model_id, 
        torch_dtype=torch.bfloat16, 
        low_cpu_mem_usage=True, 
        device_map=device,
        attn_implementation="eager"
    )
    processor = LlavaNextVideoProcessor.from_pretrained(model_id)
    
    # Process video
    video_path = "video.mp4"
    try:
        # Test if video.mp4 exists and is valid
        print(f"🔍 Testing video file: {video_path}")
        container = av.open(video_path)
        container.close()
    except Exception as e:
        print(f"⚠️ Local video '{video_path}' is invalid or missing ({e}). Downloading fallback demo video...")
        from huggingface_hub import hf_hub_download
        video_path = hf_hub_download(
            repo_id="raushan-testing-hf/videos-test",
            filename="karate.mp4",
            repo_type="dataset",
        )
        print(f"✅ Fallback video downloaded to: {video_path}")
        
    video_clip = extract_frames(video_path, num_frames=8)
    
    # Prepare prompt using the processor's chat template
    prompt_text = (
        "Sen gelişmiş bir İş Sağlığı ve Güvenliği (İSG) yapay zeka analiz uzmanısın.\n"
        "Sana verilen videoyu çok dikkatli bir şekilde analiz et. Videodaki iş kazalarını, "
        "forklift veya iş makinelerinin devrilmesini (tipping over), malzemelerin veya yapıların yıkılmasını/çökmesini (collapse), "
        "yüksekten veya düz zeminden düşmeleri (falls), sızıntıları (leakages) ve diğer tehlikeli durumları tespit et.\n"
        "Her bir olayı zaman damgasıyla (time) birlikte detaylandır.\n\n"
        "Yanıtını SADECE aşağıdaki JSON şablonuna birebir uyarak ver. JSON dışında hiçbir açıklama, "
        "giriş veya çıkış metni ekleme. Tüm listeleri ve parantezleri eksiksiz kapat.\n\n"
        "JSON Şablonu:\n"
        '{\n'
        '  "summary": "Videodaki kazanın veya olayın genel özeti (örneğin: forkliftin devrilmesi ve çevreye etkisi).",\n'
        '  "events": [\n'
        '    {"time": "00:01", "event": "Tespit edilen ilk hareket veya durum."},\n'
        '    {"time": "00:03", "event": "Kazanın gerçekleşme anı (devrilme, düşme, çarpma vb.)."}\n'
        '  ],\n'
        '  "risk": "Düşük veya Orta veya Yüksek",\n'
        '  "actions": [\n'
        '    "Kazayı önlemek veya etkisini azaltmak için alınması gereken acil önlem veya aksiyon.",\n'
        '    "Geleceğe yönelik alınması gereken İSG eğitimi ve ekipman düzenlemesi."\n'
        '  ]\n'
        '}'
    )
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "video"},
                {"type": "text", "text": prompt_text}
            ]
        }
    ]
    
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    # Force the model to start directly with the JSON opening bracket
    prompt += "{"
    
    # Process inputs
    print("⏳ Processing inputs (text + video)...")
    inputs = processor(text=prompt, videos=video_clip, return_tensors="pt").to(device)
    
    # Generate completion
    print("🧠 Running native inference on AMD GPU...")
    input_len = inputs.input_ids.shape[1]
    with torch.inference_mode():
        out = model.generate(
            **inputs, 
            max_new_tokens=1024,
            repetition_penalty=1.15
        )
        
    # Decode response (slice out the prompt tokens)
    response_text = processor.batch_decode(out[:, input_len:], skip_special_tokens=True)[0].strip()
    # Prepend the forced opening bracket back to the response
    response_text = "{" + response_text
    
    # Clean output to isolate JSON
    print("\n--- MODEL ÇIKTISI ---")
    print(response_text)
    print("---------------------\n")
    
    # Try parsing the JSON block
    try:
        # Extract everything after ASSISTANT:
        assistant_marker = "ASSISTANT:"
        if assistant_marker in response_text:
            response_json = response_text.split(assistant_marker)[-1].strip()
        else:
            response_json = response_text.strip()
            
        clean_json = response_json.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(clean_json)
        print("✅ Başarılı: Çıktı geçerli bir JSON!")
        print(f"📌 Özet: {parsed.get('summary')}")
        print(f"⚠️  Risk: {parsed.get('risk')}")
        print(f"🛠  Aksiyonlar: {', '.join(parsed.get('actions', []))}")
    except Exception as e:
        print(f"❌ JSON formatı ayrıştırılamadı: {e}")

if __name__ == "__main__":
    main()
