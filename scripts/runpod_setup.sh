#!/usr/bin/env bash
# =============================================================================
# RunPod Setup - comfyui:latest-5090 template
# =============================================================================
# ComfyUI is already installed and running on :8188.
# This script drops in custom nodes, models, workflows, and the pipeline.
#
#   git clone <repo> ~/pipeline && cd ~/pipeline
#   bash scripts/runpod_setup.sh
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# comfyui:latest-5090 paths (from config/comfyui_settings.json docker.volumes)
COMFYUI="/comfyui"
MODELS="${COMFYUI}/models"
NODES="${COMFYUI}/custom_nodes"
CIVITAI_TOKEN="${CIVITAI_API_TOKEN:-}"
HF_TOKEN="${HF_TOKEN:-}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

echo ""
echo -e "${CYAN}  AI Influencer Pipeline - RunPod Setup (comfyui:latest-5090)${NC}"
echo ""

# ---------------------------------------------------------------------------
# 1. Custom nodes
# ---------------------------------------------------------------------------
echo -e "${CYAN}[1/4] Custom nodes${NC}"

clone_node() {
    local name="$1" url="$2"
    if [[ -d "${NODES}/${name}" ]]; then
        echo -e "  ${GREEN}✓${NC} ${name}"
    else
        echo -ne "  ↓ ${name}... "
        if timeout 120 git clone --quiet --depth 1 "$url" "${NODES}/${name}" 2>/dev/null; then
            echo -e "${GREEN}ok${NC}"
        else
            echo -e "${RED}FAILED${NC} → ${url}"
        fi
    fi
    if [[ -d "${NODES}/${name}" ]]; then
        [[ -f "${NODES}/${name}/requirements.txt" ]] && timeout 120 pip install -q -r "${NODES}/${name}/requirements.txt" 2>/dev/null || true
        if [[ -f "${NODES}/${name}/install.py" ]]; then
            echo -ne "    installing ${name}... "
            if timeout 180 python3 "${NODES}/${name}/install.py" 2>/dev/null; then
                echo -e "${GREEN}done${NC}"
            else
                echo -e "${YELLOW}timeout/skip${NC}"
            fi
        fi
    fi
}

clone_node "ComfyUI-SeedVR2"             "https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler.git"
clone_node "rgthree-comfy"               "https://github.com/rgthree/rgthree-comfy.git"
clone_node "ComfyUI-Easy-Use"            "https://github.com/yolain/ComfyUI-Easy-Use.git"
clone_node "ComfyUI-Impact-Pack"         "https://github.com/ltdrdata/ComfyUI-Impact-Pack.git"
clone_node "ComfyUI-Manager"             "https://github.com/ltdrdata/ComfyUI-Manager.git"
clone_node "ComfyUI_IPAdapter_plus"      "https://github.com/cubiq/ComfyUI_IPAdapter_plus.git"
clone_node "ComfyUI-KJNodes"             "https://github.com/kijai/ComfyUI-KJNodes.git"
clone_node "comfyui_controlnet_aux"      "https://github.com/Fannovel16/comfyui_controlnet_aux.git"
clone_node "ComfyUI-WD14-Tagger"         "https://github.com/pythongosssss/ComfyUI-WD14-Tagger.git"
clone_node "ComfyUI-Florence2"           "https://github.com/kijai/ComfyUI-Florence2.git"
clone_node "ComfyUI-Crystools"           "https://github.com/crystian/ComfyUI-Crystools.git"
clone_node "ComfyUI_essentials"          "https://github.com/cubiq/ComfyUI_essentials.git"
clone_node "was-node-suite-comfyui"      "https://github.com/WASasquatch/was-node-suite-comfyui.git"

[[ -d "${NODES}/ComfyUI-Impact-Pack" ]] && (cd "${NODES}/ComfyUI-Impact-Pack" && python3 install.py 2>/dev/null) || true

# ---------------------------------------------------------------------------
# 2. Models
# ---------------------------------------------------------------------------
echo -e "${CYAN}[2/4] Models${NC}"

civitai() { echo "https://civitai.com/api/download/models/${1}"; }

dl() {
    local url="$1" dest="$2" name="$3"
    mkdir -p "$(dirname "$dest")"
    if [[ -f "$dest" ]] && [[ $(stat -c%s "$dest" 2>/dev/null || echo 0) -gt 1000000 ]]; then
        echo -e "  ${GREEN}✓${NC} ${name}"
        return 0
    fi

    local curl_args=(-L --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 1800 -o "$dest")

    # Pass auth headers if tokens are set (not required for public models)
    if [[ "$url" == *"civitai.com"* ]] && [[ -n "$CIVITAI_TOKEN" ]]; then
        curl_args+=(--header "Authorization: Bearer ${CIVITAI_TOKEN}")
    elif [[ "$url" == *"huggingface.co"* ]] && [[ -n "$HF_TOKEN" ]]; then
        curl_args+=(--header "Authorization: Bearer ${HF_TOKEN}")
    fi

    curl_args+=(--progress-bar)

    echo -e "  ↓ ${name}..."
    if curl "${curl_args[@]}" "$url"; then
        local sz=$(stat -c%s "$dest" 2>/dev/null || echo 0)
        if [[ "$sz" -gt 1000000 ]]; then
            echo -e "    ${GREEN}$(numfmt --to=iec "$sz" 2>/dev/null || echo "${sz}B")${NC}"
            return 0
        elif [[ "$sz" -gt 0 ]]; then
            local head
            head=$(head -c 200 "$dest" 2>/dev/null || true)
            if [[ "$head" == *"<html"* ]] || [[ "$head" == *"<!DOCTYPE"* ]]; then
                echo -e "    ${RED}FAILED${NC} - server returned HTML instead of model file"
                rm -f "$dest"
                return 1
            fi
            echo -e "    ${YELLOW}WARNING${NC} - only ${sz} bytes"
            return 1
        fi
    fi

    echo -e "    ${RED}FAILED${NC} - curl error (see above)"
    echo -e "    ${YELLOW}${url}${NC}"
    rm -f "$dest"
    return 1
}

# Z-Image Core (https://civitai.com/models/2168935)
dl "$(civitai 2442439)" "${MODELS}/unet/z_image_bf16.safetensors"                          "Z-Image UNet 6B" || true
dl "$(civitai 2442540)" "${MODELS}/clip/qwen_3_4b.safetensors"                             "Qwen 3.4B CLIP" || true
dl "$(civitai 2442479)" "${MODELS}/vae/ultraflux_vae.safetensors"                          "UltraFlux VAE" || true

# SeedVR2 upscaler
dl "https://huggingface.co/SeedVR/SeedVR2/resolve/main/seedvr2_ema_7b_fp16.safetensors"   "${MODELS}/upscale_models/seedvr2_ema_7b_fp16.safetensors" "SeedVR2 DiT 7B" || true
dl "https://huggingface.co/SeedVR/SeedVR2/resolve/main/ema_vae_fp16.safetensors"          "${MODELS}/vae/ema_vae_fp16.safetensors"                    "SeedVR2 VAE" || true

# Style LoRAs
dl "$(civitai 2465980)" "${MODELS}/loras/nicegirls_Zimage.safetensors"                     "nicegirls LoRA" || true
dl "$(civitai 2462523)" "${MODELS}/loras/Z-TURBO_Photography_35mmPhoto_896.safetensors"    "Z-TURBO Photo LoRA" || true
dl "$(civitai 2456035)" "${MODELS}/loras/psxZStyle_v1_ZIT.safetensors"                     "psxZStyle LoRA" || true

# SDXL for FaceDetailer pipe
dl "https://huggingface.co/digiplay/AnalogMadness-sdxl-v5/resolve/main/analogMadnessSDXL_xl5.safetensors" \
   "${MODELS}/checkpoints/analogMadnessSDXL_xl5.safetensors" "analogMadness SDXL" || true

# Face detection + segmentation
dl "https://huggingface.co/Bingsu/adetailer/resolve/main/yolov11m-face.pt"                "${MODELS}/ultralytics/YOLOV11m-face.pt" "YOLOv11m Face" || true
dl "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"                 "${MODELS}/sams/sam_vit_b_01ec64.pth"    "SAM ViT-B" || true

# ---------------------------------------------------------------------------
# 3. Deploy pipeline + workflows
# ---------------------------------------------------------------------------
echo -e "${CYAN}[3/4] Deploy pipeline${NC}"

# Workflows
mkdir -p "${COMFYUI}/user/default/workflows"
cp "${PROJECT_ROOT}/workflows/"*.json "${COMFYUI}/user/default/workflows/"
echo -e "  ${GREEN}✓${NC} Workflows"

# Pipeline (scripts, characters, config, output)
PIPELINE="${COMFYUI}/pipeline"
mkdir -p "${PIPELINE}"
cp -r "${PROJECT_ROOT}/scripts/"     "${PIPELINE}/scripts/"
cp -r "${PROJECT_ROOT}/characters/"  "${PIPELINE}/characters/"
cp -r "${PROJECT_ROOT}/config/"      "${PIPELINE}/config/"
cp -r "${PROJECT_ROOT}/output/"      "${PIPELINE}/output/" 2>/dev/null || true
echo -e "  ${GREEN}✓${NC} Pipeline → ${PIPELINE}"

# ---------------------------------------------------------------------------
# 4. Restart ComfyUI to pick up new nodes
# ---------------------------------------------------------------------------
echo -e "${CYAN}[4/4] Restart ComfyUI${NC}"

# Kill existing ComfyUI process so it restarts with new nodes loaded
COMFY_PID=$(pgrep -f "python.*main.py.*--listen" 2>/dev/null || true)
if [[ -n "$COMFY_PID" ]]; then
    echo "  Restarting ComfyUI (pid ${COMFY_PID})..."
    kill "$COMFY_PID" 2>/dev/null || true
    sleep 3
    cd "${COMFYUI}"
    PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
    CUDA_MODULE_LOADING=LAZY \
    nohup python3 main.py --listen 0.0.0.0 --port 8188 --bf16-vae --bf16-unet --fast --cuda-malloc > "${COMFYUI}/comfyui.log" 2>&1 &
    echo -ne "  Waiting"
    for i in $(seq 1 30); do
        if curl -s "http://localhost:8188/system_stats" &>/dev/null; then
            echo -e " ${GREEN}ready${NC}"
            break
        fi
        echo -n "."
        sleep 2
    done
    if ! curl -s "http://localhost:8188/system_stats" &>/dev/null; then
        echo -e " ${YELLOW}still loading${NC} → tail -f ${COMFYUI}/comfyui.log"
    fi
else
    echo -e "  ${YELLOW}No running ComfyUI found - start it manually or it should auto-start${NC}"
fi

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo ""
echo -e "${GREEN}Done.${NC} ComfyUI on http://localhost:8188"
echo ""
echo "  Generate prompts:"
echo "    cd ${PIPELINE}"
echo "    python3 scripts/prompt_engine.py master       # 21 master ref prompts"
echo "    python3 scripts/prompt_engine.py vault-all    # 21 x 800 vault prompts"
echo ""
