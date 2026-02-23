#!/usr/bin/env bash
# =============================================================================
# Download all models for the AI Influencer Pipeline
# =============================================================================
# Run on a fresh RunPod pod after cloning the repo.
#
# Usage:
#   bash scripts/download_models.sh
#
# Optional: If any CivitAI downloads fail (login-gated models), set a token:
#   export CIVITAI_API_TOKEN="your_token_here"
#   Get one at: https://civitai.com/user/account
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
COMFYUI_DIR="${COMFYUI_DIR:-/workspace/ComfyUI}"
MODELS="${COMFYUI_DIR}/models"
TOKEN="${CIVITAI_API_TOKEN:-}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

if [[ -n "$TOKEN" ]]; then
    echo -e "${GREEN}CivitAI token set${NC}"
    civitai() { echo "https://civitai.com/api/download/models/${1}?token=${TOKEN}"; }
else
    echo -e "${YELLOW}No CivitAI token - trying public downloads${NC}"
    civitai() { echo "https://civitai.com/api/download/models/${1}"; }
fi

dl() {
    local url="$1" dest="$2" name="$3"
    mkdir -p "$(dirname "$dest")"
    if [[ -f "$dest" ]] && [[ $(stat -c%s "$dest" 2>/dev/null || echo 0) -gt 1000000 ]]; then
        echo -e "  ${GREEN}✓${NC} ${name} (exists)"
        return 0
    fi
    echo -ne "  ↓ ${name}... "
    if wget -q --content-disposition -O "$dest" "$url" 2>/dev/null; then
        local sz=$(stat -c%s "$dest" 2>/dev/null || echo 0)
        echo -e "${GREEN}$(numfmt --to=iec $sz 2>/dev/null || echo "${sz}B")${NC}"
    else
        echo -e "${RED}FAILED${NC} → $url"
    fi
}

echo ""
echo -e "${CYAN}Downloading all models to: ${MODELS}${NC}"
echo ""

# ---------------------------------------------------------------------------
# Z-Image Core (CivitAI model page: https://civitai.com/models/2168935)
# ---------------------------------------------------------------------------
echo -e "${CYAN}── Z-Image Base ──${NC}"
dl "$(civitai 2442439)" \
   "${MODELS}/unet/z_image_bf16.safetensors" \
   "Z-Image UNet 6B bf16"

dl "$(civitai 2442540)" \
   "${MODELS}/clip/qwen_3_4b.safetensors" \
   "Qwen 3.4B CLIP (text encoder)"

dl "$(civitai 2442479)" \
   "${MODELS}/vae/ultraflux_vae.safetensors" \
   "UltraFlux VAE"

# ---------------------------------------------------------------------------
# SeedVR2 Upscaler (HuggingFace)
# ---------------------------------------------------------------------------
echo ""
echo -e "${CYAN}── SeedVR2 Upscaler 7B ──${NC}"
dl "https://huggingface.co/SeedVR/SeedVR2/resolve/main/seedvr2_ema_7b_fp16.safetensors" \
   "${MODELS}/upscale_models/seedvr2_ema_7b_fp16.safetensors" \
   "SeedVR2 DiT 7B fp16"

dl "https://huggingface.co/SeedVR/SeedVR2/resolve/main/ema_vae_fp16.safetensors" \
   "${MODELS}/vae/ema_vae_fp16.safetensors" \
   "SeedVR2 VAE fp16"

# ---------------------------------------------------------------------------
# Style LoRAs (CivitAI)
# ---------------------------------------------------------------------------
echo ""
echo -e "${CYAN}── Style LoRAs ──${NC}"
# NiceGirls UltraReal v1.0 - https://civitai.com/models/1862761
dl "$(civitai 2465980)" \
   "${MODELS}/loras/nicegirls_Zimage.safetensors" \
   "nicegirls_Zimage (0.45)"

# 35mm Photo - https://civitai.com/models/660731
dl "$(civitai 2462523)" \
   "${MODELS}/loras/Z-TURBO_Photography_35mmPhoto_896.safetensors" \
   "Z-TURBO Photography (0.15)"

# psxZStyle Photography - https://civitai.com/models/2076522
dl "$(civitai 2456035)" \
   "${MODELS}/loras/psxZStyle_v1_ZIT.safetensors" \
   "psxZStyle (0.10)"

# ---------------------------------------------------------------------------
# SDXL checkpoint for FaceDetailer pipe
# ---------------------------------------------------------------------------
echo ""
echo -e "${CYAN}── SDXL (FaceDetailer) ──${NC}"
dl "https://huggingface.co/digiplay/AnalogMadness-sdxl-v5/resolve/main/analogMadnessSDXL_xl5.safetensors" \
   "${MODELS}/checkpoints/analogMadnessSDXL_xl5.safetensors" \
   "analogMadness SDXL v5"

# ---------------------------------------------------------------------------
# Face detection + segmentation (Impact Pack)
# ---------------------------------------------------------------------------
echo ""
echo -e "${CYAN}── Face Detection ──${NC}"
dl "https://huggingface.co/Bingsu/adetailer/resolve/main/yolov11m-face.pt" \
   "${MODELS}/ultralytics/YOLOV11m-face.pt" \
   "YOLOv11m Face"

dl "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth" \
   "${MODELS}/sams/sam_vit_b_01ec64.pth" \
   "SAM ViT-B (segmentation)"

# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------
echo ""
echo -e "${CYAN}── Verification ──${NC}"
missing=0
while IFS=: read -r path name; do
    if [[ -f "$path" ]] && [[ $(stat -c%s "$path" 2>/dev/null || echo 0) -gt 1000000 ]]; then
        echo -e "  ${GREEN}✓${NC} ${name}"
    else
        echo -e "  ${RED}✗${NC} ${name}"
        ((missing++)) || true
    fi
done <<EOF
${MODELS}/unet/z_image_bf16.safetensors:Z-Image UNet
${MODELS}/clip/qwen_3_4b.safetensors:Qwen CLIP
${MODELS}/vae/ultraflux_vae.safetensors:UltraFlux VAE
${MODELS}/upscale_models/seedvr2_ema_7b_fp16.safetensors:SeedVR2 DiT
${MODELS}/vae/ema_vae_fp16.safetensors:SeedVR2 VAE
${MODELS}/loras/nicegirls_Zimage.safetensors:nicegirls LoRA
${MODELS}/loras/Z-TURBO_Photography_35mmPhoto_896.safetensors:Z-TURBO LoRA
${MODELS}/loras/psxZStyle_v1_ZIT.safetensors:psxZStyle LoRA
${MODELS}/checkpoints/analogMadnessSDXL_xl5.safetensors:analogMadness SDXL
${MODELS}/ultralytics/YOLOV11m-face.pt:YOLOv11m Face
${MODELS}/sams/sam_vit_b_01ec64.pth:SAM ViT-B
EOF

echo ""
if [[ $missing -gt 0 ]]; then
    echo -e "${YELLOW}${missing} model(s) missing or incomplete.${NC}"
else
    echo -e "${GREEN}All 11 models downloaded successfully.${NC}"
fi
echo ""
