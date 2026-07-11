#!/usr/bin/env bash
# TEKNOFEST 2026 Senaryo 3 — Kurulum & Çalıştırma Betiği
# vLLM öncelikli, llama.cpp/transformators fallback destekli.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="${SCRIPT_DIR}/.venv"

log() {
    echo -e "\033[1;34m[INFO]\033[0m $*"
}
warn() {
    echo -e "\033[1;33m[WARN]\033[0m $*"
}
error() {
    echo -e "\033[1;31m[ERROR]\033[0m $*" >&2
    exit 1
}

log "Çalışma dizini: ${SCRIPT_DIR}"
cd "${SCRIPT_DIR}"

# 1. Sanal ortam
if [[ ! -d "${VENV_PATH}" ]]; then
    log "Sanal ortam oluşturuluyor: ${VENV_PATH}"
    python3 -m venv "${VENV_PATH}"
fi

source "${VENV_PATH}/bin/activate"

# 2. Temel bağımlılıklar
log "Temel bağımlılıklar yükleniyor..."
pip install -q --upgrade pip setuptools wheel
pip install -q -r requirements.txt || warn "Bazı bağımlılıklar yüklenemedi; fallback modüller çalışmaya devam edecek."

# 3. llama.cpp Vulkan backend ile derle (eğer kurulu değilse)
if ! python -c "import llama_cpp" 2>/dev/null; then
    log "llama-cpp-python Vulkan backend ile derleniyor..."
    CMAKE_ARGS="-DGGML_VULKAN=on" FORCE_CMAKE=1 \
        pip install --no-cache-dir llama-cpp-python || warn "llama.cpp derlemesi başarısız; transformers/vllm fallback kullanılacak."
else
    log "llama-cpp-python zaten kurulu."
fi

# 4. Hugging Face token (.env'den oku, yoksa anonim devam et)
if [[ -f ".env" ]]; then
    export $(grep -v '^#' .env | xargs -d '\n') 2>/dev/null || true
fi

# 5. Çalıştır
VIDEO_INPUT="${1:-video.mp4}"
log "Analiz başlatılıyor: ${VIDEO_INPUT}"
python -m src.main --video "${VIDEO_INPUT}"

log "Tamamlandı. Çıktılar outputs/ dizininde."
