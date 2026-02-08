#!/usr/bin/env bash
# =============================================================================
# Download all models for the AI Influencer Pipeline
# =============================================================================
# Run on a fresh RunPod pod after cloning the repo.
#
# CivitAI models are creator-gated (free but require login):
#   export CIVITAI_API_TOKEN="your-token-here"
#   Get one at: https://civitai.com/user/account → API Keys
#
# HuggingFace models are fully public - no token needed.
# SeedVR2 models auto-download on first use, but we pre-download for reliability.
#
# Usage:
#   export CIVITAI_API_TOKEN="..."
#   bash scripts/download_models.sh
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

# Check CivitAI token (required for creator-gated models)
if [[ -z "$CIVITAI_TOKEN" ]]; then
    echo -e "${YELLOW}WARNING: CIVITAI_API_TOKEN not set.${NC}"
    echo -e "${YELLOW}CivitAI models are free but creator-gated (require login to download).${NC}"
    echo -e "${YELLOW}Get a token at: https://civitai.com/user/account → API Keys${NC}"
    echo -e "${YELLOW}Then: export CIVITAI_API_TOKEN=\"your-token\" && bash scripts/download_models.sh${NC}"
    echo ""
fi

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

    # Build curl args: follow redirects, retry on failure, long timeout for big files
    local curl_args=(-L --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 1800 -o "$dest")

    # Pass auth headers when tokens are set
    if [[ "$url" == *"civitai.com"* ]] && [[ -n "$CIVITAI_TOKEN" ]]; then
        curl_args+=(--header "Authorization: Bearer ${CIVITAI_TOKEN}")
    elif [[ "$url" == *"huggingface.co"* ]] && [[ -n "$HF_TOKEN" ]]; then
        curl_args+=(--header "Authorization: Bearer ${HF_TOKEN}")
    fi

    curl_args+=(--progress-bar)

    echo -e "  ↓ ${name}..."

    # Download - stderr shows progress bar + any errors
    if curl "${curl_args[@]}" "$url"; then
        local sz=$(stat -c%s "$dest" 2>/dev/null || echo 0)
        if [[ "$sz" -gt 1000000 ]]; then
            echo -e "    ${GREEN}$(numfmt --to=iec "$sz" 2>/dev/null || echo "${sz}B")${NC}"
            return 0
        elif [[ "$sz" -gt 0 ]]; then
            # Small file - likely an error response, not a model
            local content
            content=$(head -c 500 "$dest" 2>/dev/null || true)
            if [[ "$content" == *"<html"* ]] || [[ "$content" == *"<!DOCTYPE"* ]]; then
                echo -e "    ${RED}FAILED${NC} - server returned HTML instead of model file"
            else
                echo -e "    ${RED}FAILED${NC} - only ${sz} bytes (expected multi-MB model file)"
                echo -e "    ${YELLOW}Response: ${content}${NC}"
            fi
            echo -e "    ${YELLOW}URL: ${url}${NC}"
            rm -f "$dest"
            return 1
        fi
    fi

    echo -e "    ${RED}FAILED${NC} - curl error (see above)"
    echo -e "    ${YELLOW}${url}${NC}"
    rm -f "$dest"
    return 1
}

civitai() { echo "https://civitai.com/api/download/models/${1}"; }

# ---------------------------------------------------------------------------
# Z-Image Core (CivitAI model page: https://civitai.com/models/2168935)
# Requires CIVITAI_API_TOKEN (creator-gated)
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
# SeedVR2 Upscaler (HuggingFace - numz/SeedVR2_comfyUI)
# Public repo, no auth needed. Models go to SEEDVR2/ where the node expects them.
# The ComfyUI-SeedVR2 node also auto-downloads on first use as a fallback.
# ---------------------------------------------------------------------------
echo ""
echo -e "${CYAN}── SeedVR2 Upscaler 7B ──${NC}"
dl "https://huggingface.co/numz/SeedVR2_comfyUI/resolve/main/seedvr2_ema_7b_fp16.safetensors" \
   "${MODELS}/SEEDVR2/seedvr2_ema_7b_fp16.safetensors" \
   "SeedVR2 DiT 7B fp16" || true

dl "https://huggingface.co/numz/SeedVR2_comfyUI/resolve/main/ema_vae_fp16.safetensors" \
   "${MODELS}/SEEDVR2/ema_vae_fp16.safetensors" \
   "SeedVR2 VAE fp16" || true

# ---------------------------------------------------------------------------
# Style LoRAs (CivitAI - creator-gated)
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
# CivitAI model 408483 (Analog Madness SDXL XL5) - creator-gated
# ---------------------------------------------------------------------------
echo ""
echo -e "${CYAN}── SDXL (FaceDetailer) ──${NC}"
dl "$(civitai 2207703)" \
   "${MODELS}/checkpoints/analogMadnessSDXL_xl5.safetensors" \
   "analogMadness SDXL XL5" || true

# ---------------------------------------------------------------------------
# Face detection + segmentation (Impact Pack)
# ---------------------------------------------------------------------------
echo ""
echo -e "${CYAN}── Face Detection ──${NC}"
# face_yolov9c.pt - best available face detector from Bingsu/adetailer
# (YOLOv11m-face.pt does not exist; YOLOv9c is the best alternative)
dl "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov9c.pt" \
   "${MODELS}/ultralytics/bbox/face_yolov9c.pt" \
   "YOLOv9c Face (adetailer)" || true

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
${MODELS}/SEEDVR2/seedvr2_ema_7b_fp16.safetensors:SeedVR2 DiT
${MODELS}/SEEDVR2/ema_vae_fp16.safetensors:SeedVR2 VAE
${MODELS}/loras/nicegirls_Zimage.safetensors:nicegirls LoRA
${MODELS}/loras/Z-TURBO_Photography_35mmPhoto_896.safetensors:Z-TURBO LoRA
${MODELS}/loras/psxZStyle_v1_ZIT.safetensors:psxZStyle LoRA
${MODELS}/checkpoints/analogMadnessSDXL_xl5.safetensors:analogMadness SDXL
${MODELS}/ultralytics/bbox/face_yolov9c.pt:YOLOv9c Face
${MODELS}/sams/sam_vit_b_01ec64.pth:SAM ViT-B
EOF

echo ""
if [[ $missing -gt 0 ]]; then
    echo -e "${YELLOW}${missing} model(s) missing or incomplete.${NC}"
    if [[ -z "$CIVITAI_TOKEN" ]]; then
        echo -e "${YELLOW}Most failures are likely due to missing CIVITAI_API_TOKEN.${NC}"
        echo -e "${YELLOW}Set it and re-run: export CIVITAI_API_TOKEN=\"...\" && bash scripts/download_models.sh${NC}"
    fi
else
    echo -e "${GREEN}All 11 models downloaded successfully.${NC}"
fi
echo ""
