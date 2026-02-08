#!/usr/bin/env bash
# =============================================================================
# ONE-SHOT RunPod Setup - AI Influencer Pipeline
# =============================================================================
# Clone repo, run this, everything works. That's it.
#
#   git clone <repo> ~/pipeline && cd ~/pipeline
#   bash scripts/runpod_setup.sh
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COMFYUI_DIR="/workspace/ComfyUI"
MODELS="${COMFYUI_DIR}/models"
NODES="${COMFYUI_DIR}/custom_nodes"
TOKEN="${CIVITAI_API_TOKEN:-}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

echo ""
echo "============================================================================"
echo -e "${CYAN}  AI Influencer Pipeline - Full RunPod Setup${NC}"
echo "============================================================================"
echo ""

# ---------------------------------------------------------------------------
# 1. ComfyUI
# ---------------------------------------------------------------------------
echo -e "${CYAN}[1/6] ComfyUI${NC}"
if [[ -d "${COMFYUI_DIR}" && -f "${COMFYUI_DIR}/main.py" ]]; then
    echo -e "  ${GREEN}✓${NC} Already installed"
    (cd "${COMFYUI_DIR}" && git pull --quiet 2>/dev/null) || true
else
    echo "  Cloning ComfyUI..."
    git clone --quiet https://github.com/comfyanonymous/ComfyUI.git "${COMFYUI_DIR}"
    pip install -q -r "${COMFYUI_DIR}/requirements.txt"
    echo -e "  ${GREEN}✓${NC} Installed"
fi

# ---------------------------------------------------------------------------
# 2. Directory structure
# ---------------------------------------------------------------------------
echo -e "${CYAN}[2/6] Directories${NC}"
for d in checkpoints unet loras vae clip controlnet embeddings upscale_models ipadapter insightface ultralytics sams; do
    mkdir -p "${MODELS}/${d}"
done
mkdir -p "${COMFYUI_DIR}/output/master_images" "${COMFYUI_DIR}/output/vault"
echo -e "  ${GREEN}✓${NC} All model directories created"

# ---------------------------------------------------------------------------
# 3. Custom nodes (13 repos from comfyui_settings.json)
# ---------------------------------------------------------------------------
echo -e "${CYAN}[3/6] Custom nodes${NC}"
mkdir -p "${NODES}"

clone_node() {
    local name="$1" url="$2"
    if [[ -d "${NODES}/${name}" ]]; then
        echo -e "  ${GREEN}✓${NC} ${name}"
    else
        echo -ne "  ↓ ${name}... "
        if git clone --quiet --depth 1 "$url" "${NODES}/${name}" 2>/dev/null; then
            echo -e "${GREEN}ok${NC}"
        else
            echo -e "${RED}FAILED${NC}"
        fi
    fi
    [[ -f "${NODES}/${name}/requirements.txt" ]] && pip install -q -r "${NODES}/${name}/requirements.txt" 2>/dev/null || true
    [[ -f "${NODES}/${name}/install.py" ]] && python3 "${NODES}/${name}/install.py" 2>/dev/null || true
}

clone_node "SeedVR-ComfyUI"              "https://github.com/SeedVR/SeedVR-ComfyUI.git"
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

# Impact Pack needs its submodules
if [[ -d "${NODES}/ComfyUI-Impact-Pack" ]]; then
    (cd "${NODES}/ComfyUI-Impact-Pack" && python3 install.py 2>/dev/null) || true
fi

# ---------------------------------------------------------------------------
# 4. Download all models
# ---------------------------------------------------------------------------
echo -e "${CYAN}[4/6] Models${NC}"

if [[ -n "$TOKEN" ]]; then
    civitai() { echo "https://civitai.com/api/download/models/${1}?token=${TOKEN}"; }
else
    civitai() { echo "https://civitai.com/api/download/models/${1}"; }
fi

dl() {
    local url="$1" dest="$2" name="$3"
    if [[ -f "$dest" ]] && [[ $(stat -c%s "$dest" 2>/dev/null || echo 0) -gt 1000000 ]]; then
        echo -e "  ${GREEN}✓${NC} ${name}"
        return 0
    fi
    echo -ne "  ↓ ${name}... "
    if wget -q --content-disposition -O "$dest" "$url" 2>/dev/null; then
        local sz=$(stat -c%s "$dest" 2>/dev/null || echo 0)
        if [[ "$sz" -gt 1000000 ]]; then
            echo -e "${GREEN}$(numfmt --to=iec $sz 2>/dev/null || echo "${sz}B")${NC}"
            return 0
        fi
    fi
    echo -e "${RED}FAILED${NC}"
    echo -e "    → $url"
    return 1
}

# Z-Image Core (CivitAI model page: https://civitai.com/models/2168935)
dl "$(civitai 2442439)" "${MODELS}/unet/z_image_bf16.safetensors"                          "Z-Image UNet 6B" || true
dl "$(civitai 2442540)" "${MODELS}/clip/qwen_3_4b.safetensors"                             "Qwen 3.4B CLIP" || true
dl "$(civitai 2442479)" "${MODELS}/vae/ultraflux_vae.safetensors"                          "UltraFlux VAE" || true

# SeedVR2 upscaler (HuggingFace)
dl "https://huggingface.co/SeedVR/SeedVR2/resolve/main/seedvr2_ema_7b_fp16.safetensors"   "${MODELS}/upscale_models/seedvr2_ema_7b_fp16.safetensors" "SeedVR2 DiT 7B" || true
dl "https://huggingface.co/SeedVR/SeedVR2/resolve/main/ema_vae_fp16.safetensors"          "${MODELS}/vae/ema_vae_fp16.safetensors"                    "SeedVR2 VAE" || true

# Style LoRAs (CivitAI)
dl "$(civitai 2465980)" "${MODELS}/loras/nicegirls_Zimage.safetensors"                     "nicegirls LoRA" || true
dl "$(civitai 2462523)" "${MODELS}/loras/Z-TURBO_Photography_35mmPhoto_896.safetensors"    "Z-TURBO Photo LoRA" || true
dl "$(civitai 2456035)" "${MODELS}/loras/psxZStyle_v1_ZIT.safetensors"                     "psxZStyle LoRA" || true

# SDXL for FaceDetailer
dl "https://huggingface.co/digiplay/AnalogMadness-sdxl-v5/resolve/main/analogMadnessSDXL_xl5.safetensors" \
   "${MODELS}/checkpoints/analogMadnessSDXL_xl5.safetensors" "analogMadness SDXL" || true

# Face detection + segmentation
dl "https://huggingface.co/Bingsu/adetailer/resolve/main/yolov11m-face.pt"                "${MODELS}/ultralytics/YOLOV11m-face.pt" "YOLOv11m Face" || true
dl "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"                 "${MODELS}/sams/sam_vit_b_01ec64.pth"    "SAM ViT-B" || true

# ---------------------------------------------------------------------------
# 5. Deploy pipeline + workflows
# ---------------------------------------------------------------------------
echo -e "${CYAN}[5/6] Deploy pipeline${NC}"

# Workflows into ComfyUI
mkdir -p "${COMFYUI_DIR}/user/default/workflows"
cp "${PROJECT_ROOT}/workflows/"*.json "${COMFYUI_DIR}/user/default/workflows/" 2>/dev/null || true
echo -e "  ${GREEN}✓${NC} Workflows copied"

# Pipeline scripts/config/characters
PIPELINE="${COMFYUI_DIR}/pipeline"
mkdir -p "${PIPELINE}"
cp -r "${PROJECT_ROOT}/scripts/"     "${PIPELINE}/scripts/"
cp -r "${PROJECT_ROOT}/characters/"  "${PIPELINE}/characters/"
cp -r "${PROJECT_ROOT}/config/"      "${PIPELINE}/config/"
cp -r "${PROJECT_ROOT}/output/"      "${PIPELINE}/output/" 2>/dev/null || true
ln -sf "${PIPELINE}" "${COMFYUI_DIR}/ai_pipeline" 2>/dev/null || true
echo -e "  ${GREEN}✓${NC} Pipeline deployed to ${PIPELINE}"

# Extra model paths so ComfyUI finds everything
cat > "${COMFYUI_DIR}/extra_model_paths.yaml" <<YAML
pipeline:
    base_path: ${MODELS}
    checkpoints: checkpoints/
    unet: unet/
    clip: clip/
    vae: vae/
    loras: loras/
    upscale_models: upscale_models/
    ipadapter: ipadapter/
    insightface: insightface/
    ultralytics: ultralytics/
    embeddings: embeddings/
    controlnet: controlnet/
    sams: sams/
YAML
echo -e "  ${GREEN}✓${NC} extra_model_paths.yaml written"

# Startup script
cat > "${COMFYUI_DIR}/start.sh" <<'SH'
#!/usr/bin/env bash
cd "$(dirname "$0")"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export CUDA_MODULE_LOADING=LAZY
python3 main.py --listen 0.0.0.0 --port 8188 --bf16-vae --bf16-unet --fast --cuda-malloc --extra-model-paths-config extra_model_paths.yaml "$@"
SH
chmod +x "${COMFYUI_DIR}/start.sh"
echo -e "  ${GREEN}✓${NC} start.sh created"

# ---------------------------------------------------------------------------
# 6. Start ComfyUI
# ---------------------------------------------------------------------------
echo -e "${CYAN}[6/6] Starting ComfyUI${NC}"

if curl -s "http://localhost:8188/system_stats" &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Already running on :8188"
else
    nohup bash "${COMFYUI_DIR}/start.sh" > "${COMFYUI_DIR}/comfyui.log" 2>&1 &
    echo -ne "  Waiting for ComfyUI"
    for i in $(seq 1 30); do
        if curl -s "http://localhost:8188/system_stats" &>/dev/null; then
            echo -e " ${GREEN}ready!${NC}"
            break
        fi
        echo -n "."
        sleep 2
    done
    if ! curl -s "http://localhost:8188/system_stats" &>/dev/null; then
        echo -e " ${YELLOW}still loading - check: tail -f ${COMFYUI_DIR}/comfyui.log${NC}"
    fi
fi

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo ""
echo "============================================================================"
echo -e "${GREEN}  Done. ComfyUI running on http://localhost:8188${NC}"
echo ""
echo "  Workflows loaded from: ${COMFYUI_DIR}/user/default/workflows/"
echo "  Pipeline scripts at:   ${PIPELINE}/scripts/"
echo ""
echo "  Generate prompts:"
echo "    cd ${PIPELINE}"
echo "    python3 scripts/prompt_engine.py master        # all 21 master prompts"
echo "    python3 scripts/prompt_engine.py vault-all     # all 21 x 800 vault prompts"
echo "============================================================================"
