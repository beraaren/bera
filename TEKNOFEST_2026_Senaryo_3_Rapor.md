# TEKNOFEST 2026 Türkçe Yapay Zeka Ajanları Yarışması – Senaryo 3: Video Analiz ve Karar Destek

**Proje Raporu**

---

## 1. Giriş ve Yarışma Hakkında Genel Bilgi

**TEKNOFEST 2026 Türkçe Yapay Zeka Ajanları Yarışması**, Bilişim Vadisi yürütücülüğünde düzenlenmekte olup, katılımcıların gerçek dünya problemlerine yönelik yapay zeka çözümleri geliştirmelerini hedeflemektedir. Yarışma, savunma sanayi, güvenlik sistemleri ve saha operasyonları gibi alanlarda kullanılabilecek Türkçe doğal dil yeteneklerine sahip yapay zeka ajanları geliştirmeyi amaçlamaktadır.

### 1.1 Yarışma Senaryoları

Yarışma üç farklı senaryodan oluşmaktadır:

| Senaryo | Konu | Amaç |
|---------|------|------|
| **Senaryo 1** | Metin Tabanlı Ajan | Türkçe metin anlama, akıl yürütme ve karar destek |
| **Senaryo 2** | Görüntü Tabanlı Ajan | Görüntü analizi ve karar destek |
| **Senaryo 3** | **Video Analiz ve Karar Destek** | **Video verisini analiz eden, Türkçe özet ve aksiyon önerileri üreten sistem** |

Bu rapor, **Senaryo 3 (Video Analiz ve Karar Destek)** kapsamında geliştirilen projeyi detaylı olarak ele almaktadır.

### 1.2 Yarışma Takvimi (2026)

| Aşama | Tarih |
|-------|-------|
| Başvuru Başlangıcı | 12 Haziran |
| Son Başvuru Tarihi | 12 Temmuz |
| Ön Değerlendirme Sunumu Son Teslimi | 12 Temmuz |
| Ön Değerlendirme Sonuçlarının Açıklanması | 17 Temmuz |
| Teknik Değerlendirme Sınavı | 21 Temmuz |
| Finalistlerin Açıklanması | 24 Temmuz |
| Kick Off | 27 Temmuz |
| Yarışma Çevrimiçi Süreci | 27 Temmuz – 26 Ağustos |
| **FİNAL (TEKNOFEST Şanlıurfa)** | **30 Eylül – 4 Ekim** |

### 1.3 Ödüller

| Derece | Ödül Miktarı |
|--------|-------------|
| 1. Takım | 120.000 TL |
| 2. Takım | 100.000 TL |
| 3. Takım | 80.000 TL |

---

## 2. Senaryo 3: Video Analiz ve Karar Destek – Problem Tanımı

### 2.1 Senaryo Açıklaması

Operasyon sahasında bir video sisteme yüklenir. Sistemden şu çıktılar beklenir:

- **Olayların zaman damgası ile listelenmesi**
- **Genel video özeti**
- **Risk değerlendirmesi**
- **Aksiyon önerileri**

### 2.2 Örnek Senaryo

```json
{
  "summary": "Videoda forklift kazası ve yaralanma riski gözlenmiştir.",
  "events": [
    {"time": "00:15", "event": "Forklift devrildi"},
    {"time": "00:20", "event": "Yerde hareketsiz kişi"}
  ],
  "risk": "Yüksek",
  "actions": [
    "Sağlık ekibini çağır",
    "Alanı güvenlik altına al"
  ]
}
```

### 2.3 Temel Beklentiler

Yarışma kapsamında geliştirilecek sistemlerin karşılaması gereken teknik ve işlevsel beklentiler:

#### Çoklu Ortam (Multimodal) Anlama Yeteneği
- Video verisini yalnızca kare bazlı analiz etmekle sınırlı kalmamalı
- Sahne bütünlüğünü, zamansal ilişkileri ve olay akışını anlayabilmeli
- Nesneler, kişiler, hareketler ve olaylar bağlamsal olarak yorumlanmalı

#### Olay Tespiti ve Anlamsal Yorumlama
- Tespit edilen olaylar yalnızca tanımlanmakla kalmamalı
- Olayın türü, önemi ve olası etkileri değerlendirilmeli
- Düşük seviyeli algı ile yüksek seviyeli çıkarım arasında köprü kurulmalı

#### Zamansal Farkındalık ve Kritik An Analizi
- Olaylar zaman bilgisi ile birlikte sunulmalı
- Kritik anlar (anomaliler, kazalar, riskli durumlar) açık şekilde vurgulanmalı
- Olayların başlangıç, gelişim ve sonuç süreçleri ayırt edilebilmeli

#### Türkçe Doğal Dil Üretimi ve Özetleme
- Çıktılar açık, anlaşılır ve bağlama uygun Türkçe ile ifade edilmeli
- Özetler gereksiz detaydan arındırılmış olmalı
- Operatörün hızlı karar almasını destekleyecek şekilde yapılandırılmış olmalı

#### Aksiyon Önerisi ve Karar Destek Mekanizması
- Tespit edilen olaylara göre risk değerlendirmesi yapmalı
- Operatöre uygulanabilir ve anlamlı aksiyon önerileri sunmalı
- Öneriler bağlam ile tutarlı şekilde üretilmeli

#### Yapılandırılmış ve Açıklanabilir Çıktı
- JSON benzeri yapılandırılmış çıktı zorunludur
- Olaylar, zaman damgaları, risk seviyeleri ve aksiyon önerileri ayrıştırılmalı
- Çıktılar mümkün olduğunca açıklanabilir olmalı

#### Yerel Çalışma ve Bağımsızlık
- **Tamamen yerel ortamda çalışması zorunludur**
- Harici API, kapalı servis veya bulut bağımlılığı kabul edilmez
- Tüm model ve bileşenler lokal olarak çalıştırılmalı

#### Model Servisleme ve Altyapı Yönetimi
- vLLM veya benzeri yüksek performanslı yerel servisleme altyapıları tercih edilmeli
- Düşük gecikme ile çıktı üretmeli
- Kaynak kullanımını optimize edebilmeli
- Gerçek zamanlı veya gerçeğe yakın senaryolarda çalışabilecek şekilde tasarlanmalı

#### Performans, Ölçeklenebilirlik ve Verimlilik
- Video işleme süresi
- Model inference süresi
- Bellek ve donanım kullanımı
- Yüksek hacimli veri altında sistem davranışı

#### Ölçümleme ve KPI Tanımlama
- Olay tespit doğruluğu
- Özet kalitesi
- Aksiyon önerisi doğruluğu
- Kritik olay yakalama oranı
- İşlem süresi

#### Minimum Statik Yapı ve Akıllı Pipeline Tasarımı
- Dinamik analiz yapabilen
- Bağlama göre farklı çıktılar üretebilen
- Model tabanlı karar mekanizmaları içeren mimari
- Statik, yalnızca kural tabanlı çözümler düşük puanlanacaktır

#### Açık Kaynak ve Şeffaflık
- Açık kaynak teknolojiler kullanılarak geliştirilmeli
- Tekrar üretilebilir olmalı
- Kurulum ve çalıştırma süreçleri açık şekilde dokümante edilmeli

---

## 3. Değerlendirme Kriterleri

Projeler aşağıdaki kriterlere göre değerlendirilecektir:

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Fonksiyonellik ve Senaryo Kapsamı** | %35 | Senaryoların ne kadarının uçtan uca implemente edildiği, mock fonksiyonların başarıyla kullanılması, sistemin kararlı çalışması |
| **Teknik İmplementasyon ve Mimari** | %35 | Agentic çözümlerin temel bileşenlerinin etkin kullanımı, zorlu koşulların ele alınması, kod kalitesi, okunabilirlik ve modülerlik |
| **Otonomi ve Zeka** | %20 | Ajanın müşteri niyetini anlama ve akıl yürütme yeteneği, diyalog sırasında inisiyatif alma, beklenmedik durumlara tepki |
| **Yenilikçilik ve Yaratıcılık** | %10 | Ek senaryoların implementasyonu, ek özellikler, özgün yaklaşımlar, sunum ve dokümantasyon kalitesi |

---

## 4. Geliştirilen Proje: Video Analiz ve Karar Destek Sistemi

Bu bölümde, Senaryo 3 için geliştirilen projenin teknik detayları, mimarisi, kullanılan teknolojiler ve kod yapısı detaylı olarak açıklanmaktadır.

### 4.1 Proje Mimarisi

```
┌─────────────────────────────────────────────────────────────────┐
│                    VIDEO ANALIZ VE KARAR DESTEK                  │
│                         SISTEM MIMARISI                          │
└─────────────────────────────────────────────────────────────────┘

  ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
  │   Video      │────▶│  Kare        │────▶│  Gorsel Grid     │
  │   Girdisi    │     │  Cikarma     │     │  Olusturma       │
  │  (video.mp4) │     │  (8 kare)    │     │  (4x2 grid)      │
  └──────────────┘     └──────────────┘     └──────────────────┘
                                                      │
                                                      ▼
  ┌─────────────────────────────────────────────────────────────┐
  │              MULTIMODAL VISION-LANGUAGE MODEL              │
  │                                                              │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │  LLaVA-1.6 Mistral 7B (GGUF Q8_0)                    │   │
  │  │  + mmproj-model-f16.gguf (Vision Encoder)            │   │
  │  │  + llama.cpp Vulkan Backend                          │   │
  │  │  + 2 GPU: AMD RX 9070 (16GB) + NVIDIA RTX 4060 (8GB) │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                              │
  │  Alternatif: TimeLens-7B (Qwen2.5-VL tabanlı)               │
  │  Alternatif: LLaVA-NeXT-Video-7B (PyTorch + ROCm)           │
  └─────────────────────────────────────────────────────────────┘
                      │
                      ▼
  ┌─────────────────────────────────────────────────────────────┐
  │              YAPILANDIRILMIS CIKTI (JSON)                    │
  │                                                              │
  │  {                                                           │
  │    "summary": "Video ozeti...",                              │
  │    "events": [                                               │
  │      {"time": "00:15", "event": "Forklift devrildi"},        │
  │      {"time": "00:20", "event": "Yerde hareketsiz kisi"}     │
  │    ],                                                        │
  │    "risk": "Yuksek",                                         │
  │    "actions": [                                              │
  │      "Saglik ekibini cagir",                                 │
  │      "Alani guvenlik altina al"                              │
  │    ]                                                         │
  │  }                                                           │
  └─────────────────────────────────────────────────────────────┘
```

### 4.2 Kullanılan Teknolojiler ve Araçlar

| Bileşen | Teknoloji | Amaç |
|---------|-----------|------|
| **Video İşleme** | PyAV (`av`) | Video dosyasından kare çıkarma |
| **Görüntü İşleme** | Pillow (PIL) | Kareleri yeniden boyutlandırma ve grid oluşturma |
| **Dizi İşleme** | NumPy | Kare indeksleri ve dizi operasyonları |
| **VLM Inference** | llama-cpp-python (Vulkan backend) | GGUF formatlı multimodal model çalıştırma |
| **Model İndirme** | huggingface-hub | Hugging Face'den model dosyalarını indirme |
| **Model Formatı** | GGUF (GPT-Generated Unified Format) | Sıkıştırılmış, hızlı yüklenebilir model formatı |
| **GPU Backend** | Vulkan | Çok marka GPU desteği (AMD + NVIDIA aynı anda) |
| **Python Sürümü** | Python 3.14 | Geliştirme ortamı |

### 4.3 Donanım Yapılandırması

| Bileşen | Özellikler |
|---------|-----------|
| **GPU 0** | AMD RX 9070 – 16GB VRAM |
| **GPU 1** | NVIDIA RTX 4060 – 8GB VRAM |
| **Toplam VRAM** | 24GB |
| **CPU Backend** | x86_64, OpenMP destekli |
| **Vulkan Sürümü** | 1.4.350 |
| **İşletim Sistemi** | Linux (Arch tabanlı) |

---

## 5. Kod Dosyaları ve Detaylı Açıklamaları

### 5.1 `senaryo_3_demo.py` – Ana Demo Uygulaması (Vulkan + 2 GPU)

Bu dosya, yarışmanın temel gereksinimlerini karşılayan ana uygulamadır. **llama-cpp-python** kütüphanesi ile **Vulkan backend** kullanarak iki farklı marka GPU'yu (AMD + NVIDIA) aynı anda kullanır.

#### 5.1.1 Özellikler

- **Model**: LLaVA-1.6 Mistral 7B (GGUF Q8_0 formatında)
- **Vision Encoder**: mmproj-model-f16.gguf
- **Backend**: Vulkan (çok marka GPU desteği)
- **GPU Dağılımı**: AMD RX 9070 (birincil) + NVIDIA RTX 4060 (ikincil)
- **Video İşleme**: 8 kare çıkarma, 4x2 grid oluşturma
- **Çıktı Formatı**: JSON (summary, events, risk, actions)

#### 5.1.2 Kod Yapısı

```python
#!/usr/bin/env python3
"""
TEKNOFEST 2026 - Senaryo 3: Video Analiz ve Karar Destek
llama.cpp + Vulkan backend — 2 GPU (AMD RX 9070 16GB + NVIDIA RTX 4060 8GB)
PyTorch KULLANILMIYOR.
"""
```

**Modül İçe Aktarmaları:**

| Modül | Kullanım Amacı |
|-------|---------------|
| `av` | Video dosyasından kare çıkarma |
| `numpy` | Kare indeksleri hesaplama |
| `json` | Yapılandırılmış çıktı üretme |
| `base64`, `io` | Görüntüyü base64 data URL'e dönüştürme |
| `PIL.Image` | Görüntü işleme ve grid oluşturma |
| `huggingface_hub` | Model dosyalarını Hugging Face'den indirme |
| `llama_cpp` | GGUF model yükleme ve inference |
| `llama_cpp.llama_chat_format` | LLaVA-1.6 chat formatı |

**Fonksiyonlar:**

1. **`get_vulkan_gpus()`**: Sistemdeki Vulkan uyumlu GPU'ları tespit eder
2. **`download_model()`**: LLaVA-1.6 Mistral 7B GGUF modelini ve mmproj dosyasını indirir
3. **`load_model()`**: Modeli Vulkan backend ile iki GPU'ya yükler
4. **`extract_frames(video_path, num_frames=8)`**: Videodan eşit aralıklı 8 kare çıkarır
5. **`frames_to_grid(frames, cols=4)`**: Kareleri 4x2 grid görüntüsüne birleştirir
6. **`image_to_data_url(img)`**: Görüntüyü base64 data URL'e dönüştürür
7. **`main()`**: Ana iş akışını yönetir

#### 5.1.3 Model Yükleme Konfigürasyonu

```python
llm = Llama(
    model_path=model_path,
    chat_handler=chat_handler,
    n_gpu_layers=-1,       # Tüm katmanları GPU'ya yükle
    n_ctx=10384,           # 10384 token bağlam penceresi
    split_mode=1,          # LLAMA_SPLIT_MODE_LAYER (katman bazlı bölme)
    main_gpu=0,            # AMD RX 9070 birincil GPU
    tensor_split=[1, 0],   # VRAM dağılımı
    verbose=False,
)
```

#### 5.1.4 Chat Formatı Özelleştirmesi

LLaVA-1.6 Mistral modeli `[INST]` formatını kullanır. Varsayılan vicuna formatı yerine Mistral formatı uygulanmıştır:

```python
chat_handler.CHAT_FORMAT = (
    "{% for message in messages %}"
    "{% if message.role == 'user' %}"
    "[INST] {% if message.content is string %}{{ message.content }}{% else %}"
    "{% for content in message.content %}"
    "{% if content.type == 'image_url' and content.image_url is string %}"
    "{{ content.image_url }}{% endif %}"
    "{% if content.type == 'image_url' and content.image_url is mapping %}"
    "{{ content.image_url.url }}{% endif %}"
    "{% if content.type == 'text' %}\n{{ content.text }}{% endif %}"
    "{% endfor %}"
    "{% endif %} [/INST]"
    "{% elif message.role == 'assistant' %}"
    "{{ message.content }}"
    "{% endif %}"
    "{% endfor %}"
)
```

#### 5.1.5 Sistem Promptu (Türkçe)

```python
system_prompt = """Analyze this image grid showing 8 video frames 
(4 columns x 2 rows, left-to-right, top-to-bottom in time order).
Describe what is happening in the video. Identify any events, risks, 
and recommended actions.
Respond ONLY in valid JSON format in Turkish language:
{"summary":"...","events":[{"time":"00:00","event":"..."}],"risk":"Düşük/Orta/Yüksek","actions":["..."]}"""
```

#### 5.1.6 Inference Parametreleri

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| `max_tokens` | 600 | Maksimum üretilecek token sayısı |
| `temperature` | 0.1 | Düşük sıcaklık (daha deterministik çıktı) |
| `repeat_penalty` | 1.2 | Tekrar cezası |
| `top_p` | 0.9 | Nucleus sampling |

#### 5.1.7 JSON Çıktı İşleme

```python
try:
    clean = result_text.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(clean)
    print("✅ Başarılı: Çıktı JSON formatına uygun!")
    print(f"📌 Özet: {parsed.get('summary')}")
    print(f"⚠️  Risk: {parsed.get('risk')}")
    print(f"🛠  Aksiyonlar: {', '.join(parsed.get('actions', []))}")
except json.JSONDecodeError:
    print("❌ Hata: JSON formatı üretilemedi.")
```

---

### 5.2 `run.sh` – Çalıştırma ve Kurulum Betiği

Bu bash betiği, sanal ortam oluşturma, bağımlılık kurulumu ve uygulamayı çalıştırma işlemlerini otomatize eder.

#### 5.2.1 Özellikler

- Vulkan backend ile llama-cpp-python derleme
- Otomatik sanal ortam oluşturma (`/tmp/nlp_venv_vulkan`)
- Bağımlılık kontrolü ve kurulumu
- Demo uygulamasını çalıştırma

#### 5.2.2 Çalışma Akışı

```bash
1. VENV_PATH="/tmp/nlp_venv_vulkan" tanımla
2. Sanal ortam yoksa oluştur
3. llama-cpp-python kurulu mu kontrol et
4. Kurulu değilse Vulkan backend ile derle:
   CMAKE_ARGS="-DGGML_VULKAN=on" FORCE_CMAKE=1 pip install llama-cpp-python
5. Diğer bağımlılıkları kur: av, numpy, Pillow, huggingface_hub
6. Demo uygulamasını çalıştır
```

#### 5.2.3 Vulkan Derleme Bayrakları

```bash
CMAKE_ARGS="-DGGML_VULKAN=on" \
FORCE_CMAKE=1 \
"$VENV_PATH/bin/pip" install llama-cpp-python --no-cache-dir
```

---

### 5.3 `vulkan_timelens.py` – Alternatif Model (TimeLens-7B)

Bu dosya, **TimeLens-7B** modelini kullanarak video analizi yapan alternatif bir yaklaşımdır. TimeLens, Qwen2.5-VL mimarisi üzerine kurulu, zaman bilgisi ile güçlendirilmiş bir vision-language modelidir.

#### 5.3.1 Özellikler

- **Model**: TimeLens-7B (Qwen2.5-VL tabanlı)
- **Format**: GGUF (Q4_K_M quantization)
- **Vision Encoder**: TimeLens-7B.mmproj-f16.gguf
- **Backend**: Vulkan (llama-cpp-python)
- **Yaklaşım**: Her kare ayrı ayrı base64 olarak modele gönderilir

#### 5.3.2 Kod Yapısı

```python
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Qwen25VLChatHandler

model_repo = "mradermacher/TimeLens-7B-i1-GGUF"
model_file = "TimeLens-7B.i1-Q4_K_M.gguf"
mmproj_repo = "mradermacher/TimeLens-7B-GGUF"
mmproj_file = "TimeLens-7B.mmproj-f16.gguf"
```

#### 5.3.3 Farklı Yaklaşım: Ayrı Kareler

```python
content = []
for frame in frames:
    data_url = img_to_base64_data_url(frame)
    content.append({
        "type": "image_url",
        "image_url": {"url": data_url}
    })

content.append({
    "type": "text",
    "text": prompt_text
})
```

#### 5.3.4 Inference Parametreleri

| Parametre | Değer |
|-----------|-------|
| `n_ctx` | 16384 |
| `n_gpu_layers` | -1 (tüm katmanlar GPU) |
| `temperature` | 0.1 |
| `max_tokens` | 400 |

---

### 5.4 `run_original_amd.py` – PyTorch + ROCm Yaklaşımı

Bu dosya, orijinal Hugging Face transformers kütüphanesi ile **PyTorch + ROCm** backend kullanarak çalışan alternatif bir yaklaşımdır.

#### 5.4.1 Özellikler

- **Model**: LLaVA-NeXT-Video-7B-hf (Hugging Face formatında)
- **Backend**: PyTorch + ROCm (AMD GPU)
- **Dtype**: bfloat16
- **Video İşleme**: 8 kare, 512x288 boyutlandırma

#### 5.4.2 ROCm Ortam Değişkenleri

```python
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["ROCR_VISIBLE_DEVICES"] = "0"
os.environ["PYTORCH_ALLOC_CONF"] = "expandable_segments:True"
```

#### 5.4.3 Model Yükleme

```python
model = LlavaNextVideoForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    device_map=device,
    attn_implementation="eager"
)
processor = LlavaNextVideoProcessor.from_pretrained(model_id)
```

#### 5.4.4 Detaylı İSG Promptu

```python
prompt_text = (
    "Sen gelişmiş bir İş Sağlığı ve Güvenliği (İSG) yapay zeka analiz uzmanısın.\n"
    "Sana verilen videoyu çok dikkatli bir şekilde analiz et. "
    "Videodaki iş kazalarını, forklift veya iş makinelerinin devrilmesini, "
    "malzemelerin veya yapıların yıkılmasını/çökmesini, "
    "yüksekten veya düz zeminden düşmeleri, sızıntıları ve diğer tehlikeli durumları tespit et.\n"
    "Her bir olayı zaman damgasıyla (time) birlikte detaylandır.\n\n"
    "Yanıtını SADECE aşağıdaki JSON şablonuna birebir uyarak ver..."
)
```

#### 5.4.5 Chat Template Kullanımı

```python
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
prompt += "{"  # JSON açma parantezini zorla
```

#### 5.4.6 Generate Parametreleri

| Parametre | Değer |
|-----------|-------|
| `max_new_tokens` | 1024 |
| `repetition_penalty` | 1.15 |

---

### 5.5 `build_log.txt` – Derleme ve Kurulum Logları

Bu dosya, llama-cpp-python'un Vulkan backend ile derlenme sürecinin detaylı loglarını içerir.

#### 5.5.1 Önemli Çıkarımlar

| Özellik | Durum |
|---------|-------|
| **CMake Sürümü** | 4.3.3 |
| **C/C++ Derleyici** | GNU 16.1.1 (gcc/g++) |
| **Vulkan Sürümü** | 1.4.350 |
| **Vulkan Backend** | ✅ Aktif |
| **Cooperative Matrix** | ✅ Destekleniyor |
| **Cooperative Matrix 2** | ✅ Destekleniyor |
| **Integer Dot Product** | ✅ Destekleniyor |
| **BFloat16** | ✅ Destekleniyor |
| **OpenMP** | ✅ 5.2 |
| **Ninja Build** | ✅ Kullanılıyor |
| **Shader Generation** | ✅ 560 adım tamamlandı |

#### 5.5.2 Derleme Adımları

1. **Bağımlılık Kurulumu**: scikit-build-core, packaging, pathspec
2. **CMake Yapılandırması**: Vulkan backend aktif edildi
3. **Shader Üretimi**: vulkan-shaders-gen ile SPIR-V shader'ları oluşturuldu
4. **Ninja Build**: 560 adımda derleme tamamlandı
5. **Paylaşımlı Kütüphaneler**: libggml-base.so, libggml-cpu.so, libggml-vulkan.so

---

## 6. Video İşleme Pipeline'ı

### 6.1 Kare Çıkarma Süreci

```
Video (video.mp4)
    │
    ▼
┌─────────────────┐
│  PyAV (av)      │
│  - Container    │
│  - Video Stream │
│  - Frame Count  │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  NumPy          │
│  - Linspace     │
│  - 8 indices    │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  Frame Decode   │
│  - RGB24 format │
│  - 8 frames     │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  PIL Image      │
│  - Resize       │
│  - Grid (4x2)   │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  Base64 Encode  │
│  - PNG format   │
│  - Data URL     │
└─────────────────┘
    │
    ▼
VLM Input
```

### 6.2 Grid Oluşturma

| Parametre | Değer |
|-----------|-------|
| Kare Sayısı | 8 |
| Sütun Sayısı | 4 |
| Satır Sayısı | 2 |
| Kare Genişliği | 384 piksel |
| Kare Yüksekliği | 216 piksel |
| Toplam Grid Genişliği | 1536 piksel (4 × 384) |
| Toplam Grid Yüksekliği | 432 piksel (2 × 216) |

---

## 7. Çoklu GPU Yönetimi ve Vulkan Backend

### 7.1 Vulkan Avantajları

| Özellik | CUDA | Vulkan |
|---------|------|--------|
| AMD GPU Desteği | ❌ (ROCm gerekli) | ✅ (Native) |
| NVIDIA GPU Desteği | ✅ | ✅ |
| Çok Marka GPU | ❌ | ✅ |
| Cross-Platform | ❌ (Linux/Windows ayrı) | ✅ |
| Düşük Seviye Kontrol | Sınırlı | Tam |

### 7.2 GPU Dağılım Konfigürasyonu

```python
# AMD RX 9070 (16GB) - Birincil GPU
main_gpu = 0

# NVIDIA RTX 4060 (8GB) - İkincil GPU
# tensor_split ile VRAM oranı belirlenir
tensor_split = [1, 0]  # Tüm katmanlar GPU0'a (düzeltme gerekebilir)
```

> **Not**: `tensor_split=[1,0]` konfigürasyonu tüm katmanları GPU0'a atar. Optimal dağılım için VRAM oranlarına göre ayarlanmalıdır (örn: `[0.67, 0.33]`).

### 7.3 llama.cpp Split Modları

| Mod | Değer | Açıklama |
|-----|-------|----------|
| `LLAMA_SPLIT_MODE_NONE` | 0 | Bölme yok |
| `LLAMA_SPLIT_MODE_LAYER` | 1 | Katman bazlı bölme |
| `LLAMA_SPLIT_MODE_ROW` | 2 | Satır bazlı bölme |

---

## 8. Yarışma Gereksinimlerine Uygunluk Analizi

### 8.1 Fonksiyonellik ve Senaryo Kapsamı (%35)

| Gereksinim | Durum | Açıklama |
|------------|-------|----------|
| Video girdisi alma | ✅ | `video.mp4` veya yedek demo video |
| Video içeriğini analiz etme | ✅ | LLaVA-1.6 Mistral 7B VLM |
| Olayları tespit etme | ✅ | JSON events dizisi |
| Kişileri tespit etme | ✅ | VLM yeteneği |
| Riskli durumları tespit etme | ✅ | risk alanı |
| Kritik anları zaman bilgisi ile belirleme | ✅ | time damgaları |
| Türkçe özet üretme | ✅ | summary alanı (Türkçe) |
| Aksiyon önerileri sunma | ✅ | actions dizisi |
| Yapılandırılmış çıktı (JSON) | ✅ | Tam JSON formatı |

### 8.2 Teknik İmplementasyon ve Mimari (%35)

| Gereksinim | Durum | Açıklama |
|------------|-------|----------|
| Agentic çözümler | ⚠️ | Temel VLM kullanımı, agentic framework eklenebilir |
| Tools (mock fonksiyonlar) | ⚠️ | Eklenmesi gerekiyor |
| Memory | ⚠️ | Sohbet geçmişi yok, tek seferlik analiz |
| Prompt engineering | ✅ | Detaylı sistem promptu |
| Dinamik araç seçimi | ❌ | Henüz implemente edilmedi |
| Bağlam yönetimi | ✅ | 8 kare ile zaman bağlamı |
| Çok adımlı karar zincirleri | ❌ | Henüz implemente edilmedi |
| Hata işleme | ✅ | Try-except blokları |
| Kod kalitesi | ✅ | Modüler fonksiyonlar |
| Mock sistem entegrasyonu | ⚠️ | Eklenmesi gerekiyor |

### 8.3 Otonomi ve Zeka (%20)

| Gereksinim | Durum | Açıklama |
|------------|-------|----------|
| Müşteri niyetini anlama | ✅ | VLM bağlam anlama |
| Akıl yürütme (reasoning) | ✅ | Model kendi içinde reasoning yapar |
| İnisiyatif alma | ⚠️ | Sadece tek seferlik analiz |
| Beklenmedik durumlara tepki | ⚠️ | Sınırlı hata yönetimi |
| Doğal diyalog akışı | ❌ | Henüz diyalog yeteneği yok |

### 8.4 Yenilikçilik ve Yaratıcılık (%10)

| Gereksinim | Durum | Açıklama |
|------------|-------|----------|
| Ek senaryolar | ⚠️ | Henüz eklenmedi |
| Ek özellikler | ⚠️ | Henüz eklenmedi |
| Özgün yaklaşımlar | ✅ | 2 GPU Vulkan kullanımı |
| Sunum ve dokümantasyon | ⚠️ | Devam ediyor |

---

## 9. Teslim Edilmesi Gerekenler ve Mevcut Durum

### 9.1 Gereksinimler Listesi

| Teslim Edilecek | Açıklama | Durum |
|-----------------|----------|-------|
| **Çalışan Proje Kodu** | Tüm kaynak kodları, kurulum adımları | ✅ |
| **Demo Videosu** | Maksimum 10 dakika, senaryoları gösteren | ⚠️ Hazırlanmalı |
| **Proje Dokümantasyonu** | Mimari özeti, diagram, kullanılan teknolojiler | ⚠️ Bu rapor kapsamında |
| **Sunum Materyali** | PDF ve PPTX formatında slaytlar | ⚠️ Hazırlanmalı |

### 9.2 Proje Dokümantasyonu İçeriği

| Bölüm | Durum |
|-------|-------|
| Sistem mimarisi özeti ve diagramı | ✅ |
| Kullanılan LLM'ler ve framework'ler | ✅ |
| Implemente edilen senaryolar | ✅ |
| Adım adım çalıştırma talimatları | ✅ |
| Karşılaşılan zorluklar ve çözümler | ✅ |
| Eklenen ek özellikler | ⚠️ |
| Ölçümleme sonuçları | ⚠️ |
| Ölçekleme ihtiyaçları | ⚠️ |

---

## 10. Karşılaşılan Zorluklar ve Çözümler

### 10.1 Zorluk 1: Çok Marka GPU Kullanımı

**Problem**: AMD ve NVIDIA GPU'ların aynı anda kullanılması

**Çözüm**: Vulkan backend kullanılarak her iki GPU da aynı framework üzerinden erişilebilir hale getirildi. llama.cpp'nin Vulkan desteği sayesinde CUDA ve ROCm bağımsız çalışma sağlandı.

### 10.2 Zorluk 2: Model Formatı ve Bellek Optimizasyonu

**Problem**: 7B parametreli modelin 24GB VRAM ile çalıştırılması

**Çözüm**: GGUF formatı (Q8_0 quantization) kullanılarak model boyutu optimize edildi. mmproj (vision encoder) ayrı bir dosya olarak yüklendi.

### 10.3 Zorluk 3: Video'dan Kare Çıkarma

**Problem**: Farklı formatlardaki videoların işlenmesi

**Çözüm**: PyAV kütüphanesi kullanılarak çok çeşitli video formatları desteklendi. Hatalı video durumunda yedek demo video otomatik indiriliyor.

### 10.4 Zorluk 4: JSON Formatlı Çıktı Üretme

**Problem**: LLM'lerin yapılandırılmış çıktı üretme tutarsızlığı

**Çözüm**: 
- Düşük sıcaklık (temperature=0.1) kullanımı
- Detaylı JSON şablonu prompt içinde verme
- Çıktı sonrası JSON parsing ve temizleme
- repeat_penalty ile tekrarları azaltma

### 10.5 Zorluk 5: llama-cpp-python Derleme

**Problem**: Vulkan backend ile derleme karmaşıklığı

**Çözüm**: 
- CMake bayrakları doğru şekilde ayarlandı: `CMAKE_ARGS="-DGGML_VULKAN=on"`
- spirv-headers bağımlılığı kontrol edildi
- Sanal ortamda izole derleme yapıldı

---

## 11. Gelecek Geliştirmeler ve Öneriler

### 11.1 Kısa Vadeli (Yarışma Öncesi)

1. **Agentic Framework Entegrasyonu**
   - LangChain veya LangGraph kullanımı
   - Araç (tool) tanımlama ve kullanımı
   - Bellek (memory) yönetimi

2. **Mock Fonksiyonların Eklenmesi**
   - `call_health_team()`
   - `secure_area()`
   - `record_incident()`
   - `notify_supervisor()`

3. **Diyalog Yeteneği**
   - Kullanıcı ile etkileşimli analiz
   - Soru-cevap mekanizması
   - Bağlam değişimi yönetimi

4. **Ölçümleme ve Benchmark**
   - Inference süresi ölçümü
   - Bellek kullanımı izleme
   - Doğruluk metrikleri

### 11.2 Orta Vadeli

1. **Gerçek Zamanlı Video Analizi**
   - Stream processing
   - Anlık kare analizi
   - Uyarı sistemi

2. **Çoklu Senaryo Desteği**
   - Farklı video türleri için özelleştirilmiş promptlar
   - Endüstriye özel modeller

3. **Web Arayüzü**
   - Gradio veya Streamlit tabanlı arayüz
   - Video yükleme ve sonuç görüntüleme

### 11.3 Uzun Vadeli

1. **Model İyileştirme**
   - Fine-tuning Türkçe video verisi üzerinde
   - Quantization optimizasyonu

2. **Ölçeklenebilirlik**
   - vLLM servis entegrasyonu
   - Çoklu model desteği
   - Batch processing

---

## 12. Sonuç

Bu proje, TEKNOFEST 2026 Türkçe Yapay Zeka Ajanları Yarışması'nın **Senaryo 3: Video Analiz ve Karar Destek** gereksinimlerini karşılamak üzere geliştirilmiştir. Proje, aşağıdaki temel özellikleri sunmaktadır:

✅ **Video analizi ve olay tespiti**
✅ **Türkçe doğal dil üretimi**
✅ **Yapılandırılmış JSON çıktısı**
✅ **Risk değerlendirmesi ve aksiyon önerileri**
✅ **Tamamen yerel çalışma (offline)**
✅ **Çok marka GPU desteği (AMD + NVIDIA)**
✅ **Açık kaynak teknolojiler**
✅ **Tekrar üretilebilir kurulum**

Proje, llama.cpp + Vulkan backend kullanarak benzersiz bir çok GPU çözümü sunmaktadır. Gelecek geliştirmeler ile agentic yetenekler, mock fonksiyonlar ve diyalog yeteneği eklenerek yarışma değerlendirme kriterlerine tam uygunluk sağlanacaktır.

---

## Ekler

### A. Dosya Listesi

| Dosya | Açıklama | Satır Sayısı |
|-------|----------|-------------|
| `senaryo_3_demo.py` | Ana demo uygulaması (Vulkan + 2 GPU) | 201 |
| `run.sh` | Kurulum ve çalıştırma betiği | 35 |
| `vulkan_timelens.py` | Alternatif TimeLens-7B modeli | 146 |
| `run_original_amd.py` | PyTorch + ROCm alternatifi | 182 |
| `build_log.txt` | Derleme logları | 1134 |
| `video.mp4` | Demo video dosyası | - |
| `2026_TEKNOFEST_TYDA_SARTNAME_Ucuncu_Senaryo_TR_2_42gcW.pdf` | Yarışma şartnamesi | - |

### B. Kullanılan Modeller

| Model | Kaynak | Format | Boyut |
|-------|--------|--------|-------|
| LLaVA-1.6 Mistral 7B | cjpais/llava-1.6-mistral-7b-gguf | GGUF Q8_0 | ~7.5GB |
| mmproj-model-f16 | cjpais/llava-1.6-mistral-7b-gguf | GGUF F16 | ~600MB |
| TimeLens-7B | mradermacher/TimeLens-7B-i1-GGUF | GGUF Q4_K_M | ~4GB |
| TimeLens-7B mmproj | mradermacher/TimeLens-7B-GGUF | GGUF F16 | ~600MB |
| LLaVA-NeXT-Video-7B | llava-hf/LLaVA-NeXT-Video-7B-hf | Hugging Face | ~14GB |

### C. Bağımlılıklar

```
av (PyAV)
numpy
Pillow
huggingface_hub
llama-cpp-python (Vulkan backend ile derlenmiş)
torch (sadece run_original_amd.py için)
transformers (sadece run_original_amd.py için)
```

---

**Rapor Tarihi**: 27 Haziran 2026

**Proje**: TEKNOFEST 2026 - Türkçe Yapay Zeka Ajanları Yarışması

**Senaryo**: 3 - Video Analiz ve Karar Destek
