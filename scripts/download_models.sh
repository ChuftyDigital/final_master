#!/usr/bin/env bash
# =============================================================================
# Download all models for the AI Influencer Pipeline
# =============================================================================
# Run on a fresh RunPod pod after cloning the repo.
#
# Usage:
#   bash scripts/download_models.sh
#
# Optional tokens for gated/login-required models:
#   export CIVITAI_API_TOKEN="your_token"    # https://civitai.com/user/account
#   export HF_TOKEN="your_token"             # https://huggingface.co/settings/tokens
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
# RunPod comfyui:latest-5090 template uses /comfyui
COMFYUI_DIR="${COMFYUI_DIR:-/comfyui}"
MODELS="${COMFYUI_DIR}/models"
CIVITAI_TOKEN="${CIVITAI_API_TOKEN:-}"
HF_TOKEN="${HF_TOKEN:-}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

echo ""
echo -e "${CYAN}Downloading all models to: ${MODELS}${NC}"
echo ""

if [[ -n "$CIVITAI_TOKEN" ]]; then
    echo -e "  ${GREEN}CivitAI token set${NC}"
else
    echo -e "  ${YELLOW}No CIVITAI_API_TOKEN - some CivitAI downloads may fail if login-gated${NC}"
fi
if [[ -n "$HF_TOKEN" ]]; then
    echo -e "  ${GREEN}HuggingFace token set${NC}"
else
    echo -e "  ${YELLOW}No HF_TOKEN - some HuggingFace downloads may fail if gated${NC}"
fi
echo ""

# ---------------------------------------------------------------------------
# Download function using curl with proper error handling
# ---------------------------------------------------------------------------
dl() {
    local url="$1" dest="$2" name="$3"
    mkdir -p "$(dirname "$dest")"

    # Skip if already downloaded (>1MB = real file, not error page)
    if [[ -f "$dest" ]] && [[ $(stat -c%s "$dest" 2>/dev/null || echo 0) -gt 1000000 ]]; then
        echo -e "  ${GREEN}✓${NC} ${name} (exists)"
        return 0
    fi

    # Build curl args
    local curl_args=(-L --fail --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 1800 -o "$dest")

    # Add auth headers based on URL
    if [[ "$url" == *"civitai.com"* ]] && [[ -n "$CIVITAI_TOKEN" ]]; then
        curl_args+=(--header "Authorization: Bearer ${CIVITAI_TOKEN}")
    elif [[ "$url" == *"huggingface.co"* ]] && [[ -n "$HF_TOKEN" ]]; then
        curl_args+=(--header "Authorization: Bearer ${HF_TOKEN}")
    fi

    # Show progress for large files
    curl_args+=(--progress-bar)

    echo -ne "  ↓ ${name}... "

    # Download with full error output visible
    local http_code
    if curl "${curl_args[@]}" "$url" 2>&1; then
        local sz=$(stat -c%s "$dest" 2>/dev/null || echo 0)
        # Verify it's not a tiny error page
        if [[ "$sz" -gt 1000000 ]]; then
            echo -e "  ${GREEN}$(numfmt --to=iec "$sz" 2>/dev/null || echo "${sz}B")${NC}"
            return 0
        elif [[ "$sz" -gt 0 ]]; then
            # Small file - likely an HTML error page
            local head
            head=$(head -c 200 "$dest" 2>/dev/null || true)
            if [[ "$head" == *"<html"* ]] || [[ "$head" == *"<!DOCTYPE"* ]] || [[ "$head" == *"login"* ]]; then
                echo -e "${RED}FAILED${NC} - got HTML error page (auth required?)"
                echo -e "    ${YELLOW}URL: ${url}${NC}"
                rm -f "$dest"
                return 1
            else
                echo -e "${YELLOW}WARNING${NC} - file is only ${sz} bytes"
                return 1
            fi
        fi
    fi

    echo -e "${RED}FAILED${NC}"
    echo -e "    ${YELLOW}URL: ${url}${NC}"
    rm -f "$dest"
    return 1
}

# CivitAI URL builder (token via header now, not query param)
civitai() { echo "https://civitai.com/api/download/models/${1}"; }

# ---------------------------------------------------------------------------
# Z-Image Core (CivitAI model page: https://civitai.com/models/2168935)
# ---------------------------------------------------------------------------
echo -e "${CYAN}── Z-Image Base ──${NC}"
dl "$(civitai 2442439)" \
   "${MODELS}/unet/z_image_bf16.safetensors" \
   "Z-Image UNet 6B bf16" || true

dl "$(civitai 2442540)" \
   "${MODELS}/clip/qwen_3_4b.safetensors" \
   "Qwen 3.4B CLIP (text encoder)" || true

dl "$(civitai 2442479)" \
   "${MODELS}/vae/ultraflux_vae.safetensors" \
   "UltraFlux VAE" || true

# ---------------------------------------------------------------------------
# SeedVR2 Upscaler (HuggingFace)
# ---------------------------------------------------------------------------
echo ""
echo -e "${CYAN}── SeedVR2 Upscaler 7B ──${NC}"
dl "https://huggingface.co/SeedVR/SeedVR2/resolve/main/seedvr2_ema_7b_fp16.safetensors" \
   "${MODELS}/upscale_models/seedvr2_ema_7b_fp16.safetensors" \
   "SeedVR2 DiT 7B fp16" || true

dl "https://huggingface.co/SeedVR/SeedVR2/resolve/main/ema_vae_fp16.safetensors" \
   "${MODELS}/vae/ema_vae_fp16.safetensors" \
   "SeedVR2 VAE fp16" || true

# ---------------------------------------------------------------------------
# Style LoRAs (CivitAI)
# ---------------------------------------------------------------------------
echo ""
echo -e "${CYAN}── Style LoRAs ──${NC}"
# NiceGirls UltraReal v1.0 - https://civitai.com/models/1862761
dl "$(civitai 2465980)" \
   "${MODELS}/loras/nicegirls_Zimage.safetensors" \
   "nicegirls_Zimage (0.45)" || true

# 35mm Photo - https://civitai.com/models/660731
dl "$(civitai 2462523)" \
   "${MODELS}/loras/Z-TURBO_Photography_35mmPhoto_896.safetensors" \
   "Z-TURBO Photography (0.15)" || true

# psxZStyle Photography - https://civitai.com/models/2076522
dl "$(civitai 2456035)" \
   "${MODELS}/loras/psxZStyle_v1_ZIT.safetensors" \
   "psxZStyle (0.10)" || true

# ---------------------------------------------------------------------------
# SDXL checkpoint for FaceDetailer pipe
# ---------------------------------------------------------------------------
echo ""
echo -e "${CYAN}── SDXL (FaceDetailer) ──${NC}"
dl "https://huggingface.co/digiplay/AnalogMadness-sdxl-v5/resolve/main/analogMadnessSDXL_xl5.safetensors" \
   "${MODELS}/checkpoints/analogMadnessSDXL_xl5.safetensors" \
   "analogMadness SDXL v5" || true

# ---------------------------------------------------------------------------
# Face detection + segmentation (Impact Pack)
# ---------------------------------------------------------------------------
echo ""
echo -e "${CYAN}── Face Detection ──${NC}"
dl "https://huggingface.co/Bingsu/adetailer/resolve/main/yolov11m-face.pt" \
   "${MODELS}/ultralytics/YOLOV11m-face.pt" \
   "YOLOv11m Face" || true

dl "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth" \
   "${MODELS}/sams/sam_vit_b_01ec64.pth" \
   "SAM ViT-B (segmentation)" || true

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
${MODELS}/loras/nicegirls_Zimage.safetensors:nicegirles LoRA
${MODELS}/loras/Z-TURBO_Photography_35mmPhoto_896.safetensors:Z-TURBO LoRA
${MODELS}/loras/psxZStyle_v1_ZIT.safetensors:psxZStyle LoRA
${MODELS}/checkpoints/analogMadnessSDXL_xl5.safetensors:analogMadness SDXL
${MODELS}/ultralytics/YOLOV11m-face.pt:YOLOv11m Face
${MODELS}/sams/sam_vit_b_01ec64.pth:SAM ViT-B
EOF

echo ""
if [[ $missing -gt 0 ]]; then
    echo -e "${YELLOW}${missing} model(s) missing or incomplete.${NC}"
    echo ""
    echo -e "Troubleshooting:"
    echo -e "  - CivitAI models may need a token: export CIVITAI_API_TOKEN=\"your_token\""
    echo -e "  - HuggingFace gated models need: export HF_TOKEN=\"your_token\""
    echo -e "  - Check if model pages require accepting terms first"
else
    echo -e "${GREEN}All 11 models downloaded successfully.${NC}"
fi
echo ""
