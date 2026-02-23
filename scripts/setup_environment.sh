#!/usr/bin/env bash
# =============================================================================
# RunPod Setup - AI Influencer Image Generation Pipeline
# =============================================================================
#
# Deploys the complete pipeline to a fresh RunPod GPU pod:
#   1. Installs ComfyUI (if not present)
#   2. Clones all 13+ required custom nodes
#   3. Downloads all Z-Image Base models to correct paths
#   4. Deploys workflows, prompt engine, characters, and configs
#   5. Starts ComfyUI with RTX 5090 / bf16 optimizations
#
# Usage (on a fresh RunPod pod):
#   git clone <your-repo> ~/pipeline && cd ~/pipeline
#   chmod +x scripts/setup_environment.sh
#   ./scripts/setup_environment.sh
#
# Flags:
#   --skip-comfyui    Skip ComfyUI installation (already installed)
#   --skip-nodes      Skip custom node cloning
#   --skip-models     Skip model downloads
#   --skip-start      Don't auto-start ComfyUI at the end
#   --comfyui-dir     Path to existing ComfyUI install (default: /workspace/ComfyUI)
#
# Requirements:
#   - RunPod GPU pod with NVIDIA drivers + CUDA
#   - ~120GB free disk (models + ComfyUI + custom nodes)
#   - Internet access for git clones and model downloads
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default ComfyUI location (RunPod standard)
COMFYUI_DIR="/workspace/ComfyUI"
COMFYUI_PORT=8188

# Colour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }
log_step()  { echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"; echo -e "${CYAN}  $*${NC}"; echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"; }

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
SKIP_COMFYUI=false
SKIP_NODES=false
SKIP_MODELS=false
SKIP_START=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --skip-comfyui) SKIP_COMFYUI=true; shift ;;
        --skip-nodes)   SKIP_NODES=true; shift ;;
        --skip-models)  SKIP_MODELS=true; shift ;;
        --skip-start)   SKIP_START=true; shift ;;
        --comfyui-dir)  COMFYUI_DIR="$2"; shift 2 ;;
        -h|--help)
            echo "Usage: $0 [--skip-comfyui] [--skip-nodes] [--skip-models] [--skip-start] [--comfyui-dir PATH]"
            exit 0
            ;;
        *) log_error "Unknown option: $1"; exit 1 ;;
    esac
done

# Model directories (relative to ComfyUI)
MODELS_DIR="${COMFYUI_DIR}/models"
NODES_DIR="${COMFYUI_DIR}/custom_nodes"

echo ""
echo "============================================================================"
echo -e "${CYAN}  AI Influencer Pipeline - RunPod Setup${NC}"
echo "============================================================================"
echo "  Project:    ${PROJECT_ROOT}"
echo "  ComfyUI:    ${COMFYUI_DIR}"
echo "  Models:     ${MODELS_DIR}"
echo "============================================================================"
echo ""

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------
log_step "Pre-flight checks"

if command -v nvidia-smi &>/dev/null; then
    GPU_NAME=$(nvidia-smi --query-gpu=gpu_name --format=csv,noheader 2>/dev/null | head -1 || echo "unknown")
    GPU_VRAM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1 || echo "0")
    log_info "GPU: ${GPU_NAME} (${GPU_VRAM} MiB VRAM)"
    if [[ "$GPU_VRAM" -lt 20000 ]]; then
        log_warn "Pipeline optimised for 32GB VRAM (RTX 5090). Detected: ${GPU_VRAM} MiB."
        log_warn "Z-Image Base (6B) + SeedVR2 (7B) needs ~24GB minimum."
    fi
else
    log_warn "nvidia-smi not found. Make sure you're on a GPU pod."
fi

if command -v python3 &>/dev/null; then
    log_info "Python: $(python3 --version 2>&1)"
else
    log_error "Python 3 not found."
    exit 1
fi

log_info "Disk space: $(df -h /workspace 2>/dev/null | tail -1 | awk '{print $4 " available"}' || echo "unknown")"

# ---------------------------------------------------------------------------
# Step 1: Install ComfyUI
# ---------------------------------------------------------------------------
if [[ "$SKIP_COMFYUI" == false ]]; then
    log_step "Step 1: Installing ComfyUI"

    if [[ -d "${COMFYUI_DIR}" && -f "${COMFYUI_DIR}/main.py" ]]; then
        log_info "ComfyUI already exists at ${COMFYUI_DIR}"
        log_info "Pulling latest updates..."
        (cd "${COMFYUI_DIR}" && git pull --quiet 2>/dev/null) || log_warn "Could not update ComfyUI"
    else
        log_info "Cloning ComfyUI to ${COMFYUI_DIR}..."
        git clone https://github.com/comfyanonymous/ComfyUI.git "${COMFYUI_DIR}"
        log_info "Installing ComfyUI Python dependencies..."
        pip install -q -r "${COMFYUI_DIR}/requirements.txt"
    fi

    log_info "ComfyUI ready at: ${COMFYUI_DIR}"
else
    log_info "Skipping ComfyUI install (--skip-comfyui)"
fi

# ---------------------------------------------------------------------------
# Step 2: Create directory structure
# ---------------------------------------------------------------------------
log_step "Step 2: Creating directory structure"

DIRECTORIES=(
    "${MODELS_DIR}/checkpoints"
    "${MODELS_DIR}/unet"
    "${MODELS_DIR}/loras"
    "${MODELS_DIR}/vae"
    "${MODELS_DIR}/clip"
    "${MODELS_DIR}/controlnet"
    "${MODELS_DIR}/embeddings"
    "${MODELS_DIR}/upscale_models"
    "${MODELS_DIR}/ipadapter"
    "${MODELS_DIR}/insightface"
    "${MODELS_DIR}/ultralytics"
    "${COMFYUI_DIR}/input"
    "${COMFYUI_DIR}/output"
    "${COMFYUI_DIR}/output/master_images"
    "${COMFYUI_DIR}/output/vault"
)

for dir in "${DIRECTORIES[@]}"; do
    mkdir -p "$dir"
done

log_info "Directory structure created."

# ---------------------------------------------------------------------------
# Step 3: Install Custom Nodes
# ---------------------------------------------------------------------------
if [[ "$SKIP_NODES" == false ]]; then
    log_step "Step 3: Installing custom nodes (13 repos)"

    mkdir -p "${NODES_DIR}"

    # All custom nodes from config/comfyui_settings.json + workflow requirements
    declare -A CUSTOM_NODES=(
        # From comfyui_settings.json
        ["SeedVR-ComfyUI"]="https://github.com/SeedVR/SeedVR-ComfyUI.git"
        ["rgthree-comfy"]="https://github.com/rgthree/rgthree-comfy.git"
        ["ComfyUI-Easy-Use"]="https://github.com/yolain/ComfyUI-Easy-Use.git"
        ["ComfyUI-Impact-Pack"]="https://github.com/ltdrdata/ComfyUI-Impact-Pack.git"
        ["ComfyUI-Manager"]="https://github.com/ltdrdata/ComfyUI-Manager.git"
        ["ComfyUI_IPAdapter_plus"]="https://github.com/cubiq/ComfyUI_IPAdapter_plus.git"
        ["ComfyUI-KJNodes"]="https://github.com/kijai/ComfyUI-KJNodes.git"
        ["comfyui_controlnet_aux"]="https://github.com/Fannovel16/comfyui_controlnet_aux.git"
        ["ComfyUI-WD14-Tagger"]="https://github.com/pythongosssss/ComfyUI-WD14-Tagger.git"
        ["ComfyUI-Florence2"]="https://github.com/kijai/ComfyUI-Florence2.git"
        ["ComfyUI-Crystools"]="https://github.com/crystian/ComfyUI-Crystools.git"
        ["ComfyUI_essentials"]="https://github.com/cubiq/ComfyUI_essentials.git"
        ["was-node-suite-comfyui"]="https://github.com/WASasquatch/was-node-suite-comfyui.git"
    )

    installed=0
    failed=0

    for node_name in "${!CUSTOM_NODES[@]}"; do
        node_dir="${NODES_DIR}/${node_name}"
        repo_url="${CUSTOM_NODES[${node_name}]}"

        if [[ -d "$node_dir" ]]; then
            echo -n "  Updating ${node_name}... "
            if (cd "$node_dir" && git pull --quiet 2>/dev/null); then
                echo -e "${GREEN}ok${NC}"
            else
                echo -e "${YELLOW}skip${NC}"
            fi
        else
            echo -n "  Cloning ${node_name}... "
            if git clone --quiet --depth 1 "$repo_url" "$node_dir" 2>/dev/null; then
                echo -e "${GREEN}ok${NC}"
                ((installed++))
            else
                echo -e "${RED}FAILED${NC}"
                ((failed++))
            fi
        fi

        # Install node-specific Python deps
        if [[ -f "${node_dir}/requirements.txt" ]]; then
            pip install -q -r "${node_dir}/requirements.txt" 2>/dev/null || true
        fi
        if [[ -f "${node_dir}/install.py" ]]; then
            python3 "${node_dir}/install.py" 2>/dev/null || true
        fi
    done

    log_info "Custom nodes: ${installed} installed, ${failed} failed"

    # Impact Pack submodules (needed for FaceDetailer)
    if [[ -d "${NODES_DIR}/ComfyUI-Impact-Pack" ]]; then
        log_info "Installing Impact Pack submodules..."
        (cd "${NODES_DIR}/ComfyUI-Impact-Pack" && python3 install.py 2>/dev/null) || true
    fi
else
    log_info "Skipping custom nodes (--skip-nodes)"
fi

# ---------------------------------------------------------------------------
# Step 4: Download Models
# ---------------------------------------------------------------------------
if [[ "$SKIP_MODELS" == false ]]; then
    log_step "Step 4: Downloading models"

    # Helper function for downloads with retry
    download_model() {
        local url="$1"
        local dest="$2"
        local name="$3"

        if [[ -f "$dest" ]]; then
            local size=$(stat -c%s "$dest" 2>/dev/null || stat -f%z "$dest" 2>/dev/null || echo "0")
            if [[ "$size" -gt 1000000 ]]; then
                echo -e "  ${GREEN}✓${NC} ${name} (already downloaded, $(numfmt --to=iec $size 2>/dev/null || echo "${size} bytes"))"
                return 0
            fi
        fi

        echo -n "  Downloading ${name}... "
        local retries=3
        for ((i=1; i<=retries; i++)); do
            if wget -q --show-progress -O "$dest" "$url" 2>/dev/null || \
               curl -sL -o "$dest" "$url" 2>/dev/null; then
                local size=$(stat -c%s "$dest" 2>/dev/null || stat -f%z "$dest" 2>/dev/null || echo "0")
                echo -e "${GREEN}ok${NC} ($(numfmt --to=iec $size 2>/dev/null || echo "${size} bytes"))"
                return 0
            fi
            [[ $i -lt $retries ]] && sleep $((i * 2))
        done

        echo -e "${RED}FAILED${NC}"
        echo -e "    ${YELLOW}Manual download required:${NC} $url"
        echo -e "    ${YELLOW}Place at:${NC} $dest"
        return 1
    }

    echo ""
    echo "  ┌─────────────────────────────────────────────────────────────┐"
    echo "  │  Z-Image Base Pipeline Models                              │"
    echo "  │  Total: ~80GB across 10 model files                       │"
    echo "  └─────────────────────────────────────────────────────────────┘"
    echo ""

    # -----------------------------------------------------------------------
    # CORE MODELS - Z-Image Base (6B)
    # -----------------------------------------------------------------------
    echo -e "  ${CYAN}── Core Models (Z-Image Base 6B) ──${NC}"

    # Z-Image Base UNet (6B params, bf16)
    # NOTE: Update these URLs to your actual model hosting locations
    # CivitAI models need an API key: --header "Authorization: Bearer YOUR_KEY"
    download_model \
        "PLACEHOLDER_URL/z_image_bf16.safetensors" \
        "${MODELS_DIR}/unet/z_image_bf16.safetensors" \
        "Z-Image Base UNet (6B, bf16)" || true

    # Qwen CLIP encoder for Z-Image
    download_model \
        "PLACEHOLDER_URL/qwen_3_4b.safetensors" \
        "${MODELS_DIR}/clip/qwen_3_4b.safetensors" \
        "Qwen 3.4B CLIP (lumina2)" || true

    # UltraFlux VAE
    download_model \
        "PLACEHOLDER_URL/ultraflux_vae.safetensors" \
        "${MODELS_DIR}/vae/ultraflux_vae.safetensors" \
        "UltraFlux VAE" || true

    # -----------------------------------------------------------------------
    # UPSCALER - SeedVR2 (7B)
    # -----------------------------------------------------------------------
    echo ""
    echo -e "  ${CYAN}── SeedVR2 Upscaler (7B) ──${NC}"

    download_model \
        "PLACEHOLDER_URL/seedvr2_ema_7b_fp16.safetensors" \
        "${MODELS_DIR}/upscale_models/seedvr2_ema_7b_fp16.safetensors" \
        "SeedVR2 DiT (7B, fp16)" || true

    download_model \
        "PLACEHOLDER_URL/ema_vae_fp16.safetensors" \
        "${MODELS_DIR}/vae/ema_vae_fp16.safetensors" \
        "SeedVR2 VAE (fp16)" || true

    # -----------------------------------------------------------------------
    # STYLE LORAS
    # -----------------------------------------------------------------------
    echo ""
    echo -e "  ${CYAN}── Style LoRAs ──${NC}"

    download_model \
        "PLACEHOLDER_URL/nicegirls_Zimage.safetensors" \
        "${MODELS_DIR}/loras/nicegirls_Zimage.safetensors" \
        "nicegirls_Zimage LoRA (0.45)" || true

    download_model \
        "PLACEHOLDER_URL/Z-TURBO_Photography_35mmPhoto_896.safetensors" \
        "${MODELS_DIR}/loras/Z-TURBO_Photography_35mmPhoto_896.safetensors" \
        "Z-TURBO Photography LoRA (0.15)" || true

    download_model \
        "PLACEHOLDER_URL/psxZStyle_v1_ZIT.safetensors" \
        "${MODELS_DIR}/loras/psxZStyle_v1_ZIT.safetensors" \
        "psxZStyle LoRA (0.10)" || true

    # -----------------------------------------------------------------------
    # SDXL AUXILIARY (for FaceDetailer pipe)
    # -----------------------------------------------------------------------
    echo ""
    echo -e "  ${CYAN}── SDXL Auxiliary ──${NC}"

    download_model \
        "PLACEHOLDER_URL/analogMadnessSDXL_xl5.safetensors" \
        "${MODELS_DIR}/checkpoints/analogMadnessSDXL_xl5.safetensors" \
        "analogMadness SDXL v5 (FaceDetailer)" || true

    # -----------------------------------------------------------------------
    # FACE DETECTION
    # -----------------------------------------------------------------------
    echo ""
    echo -e "  ${CYAN}── Face Detection ──${NC}"

    download_model \
        "PLACEHOLDER_URL/YOLOV11m-face.pt" \
        "${MODELS_DIR}/ultralytics/YOLOV11m-face.pt" \
        "YOLOv11m Face Detector" || true

    echo ""

    # -----------------------------------------------------------------------
    # Model verification
    # -----------------------------------------------------------------------
    echo -e "  ${CYAN}── Model Verification ──${NC}"
    REQUIRED_MODELS=(
        "${MODELS_DIR}/unet/z_image_bf16.safetensors:Z-Image Base UNet"
        "${MODELS_DIR}/clip/qwen_3_4b.safetensors:Qwen CLIP"
        "${MODELS_DIR}/vae/ultraflux_vae.safetensors:UltraFlux VAE"
        "${MODELS_DIR}/upscale_models/seedvr2_ema_7b_fp16.safetensors:SeedVR2 DiT"
        "${MODELS_DIR}/vae/ema_vae_fp16.safetensors:SeedVR2 VAE"
        "${MODELS_DIR}/loras/nicegirls_Zimage.safetensors:nicegirls LoRA"
        "${MODELS_DIR}/loras/Z-TURBO_Photography_35mmPhoto_896.safetensors:Z-TURBO LoRA"
        "${MODELS_DIR}/loras/psxZStyle_v1_ZIT.safetensors:psxZStyle LoRA"
        "${MODELS_DIR}/checkpoints/analogMadnessSDXL_xl5.safetensors:analogMadness SDXL"
        "${MODELS_DIR}/ultralytics/YOLOV11m-face.pt:YOLOv11m Face"
    )

    missing=0
    for entry in "${REQUIRED_MODELS[@]}"; do
        path="${entry%%:*}"
        name="${entry##*:}"
        if [[ -f "$path" ]]; then
            local_size=$(stat -c%s "$path" 2>/dev/null || stat -f%z "$path" 2>/dev/null || echo "0")
            if [[ "$local_size" -gt 1000000 ]]; then
                echo -e "  ${GREEN}✓${NC} ${name}"
            else
                echo -e "  ${RED}✗${NC} ${name} (file too small, likely incomplete)"
                ((missing++))
            fi
        else
            echo -e "  ${RED}✗${NC} ${name} - MISSING"
            ((missing++))
        fi
    done

    echo ""
    if [[ $missing -gt 0 ]]; then
        log_warn "${missing} model(s) missing. Replace PLACEHOLDER_URL entries in this script"
        log_warn "with your actual download URLs (CivitAI, HuggingFace, etc.) and re-run."
        log_warn "Or download manually and place in the paths shown above."
    else
        log_info "All 10 models verified!"
    fi
else
    log_info "Skipping model downloads (--skip-models)"
fi

# ---------------------------------------------------------------------------
# Step 5: Deploy Pipeline Files
# ---------------------------------------------------------------------------
log_step "Step 5: Deploying pipeline files to ComfyUI"

# Copy workflows to ComfyUI
log_info "Copying workflows..."
mkdir -p "${COMFYUI_DIR}/user/default/workflows"
cp -v "${PROJECT_ROOT}/workflows/"*.json "${COMFYUI_DIR}/user/default/workflows/" 2>/dev/null || \
    cp -v "${PROJECT_ROOT}/workflows/"*.json "${COMFYUI_DIR}/workflows/" 2>/dev/null || true

# Copy pipeline scripts
log_info "Copying pipeline scripts..."
PIPELINE_DIR="${COMFYUI_DIR}/pipeline"
mkdir -p "${PIPELINE_DIR}"
cp -r "${PROJECT_ROOT}/scripts/" "${PIPELINE_DIR}/scripts/"
cp -r "${PROJECT_ROOT}/characters/" "${PIPELINE_DIR}/characters/"
cp -r "${PROJECT_ROOT}/config/" "${PIPELINE_DIR}/config/"
cp -r "${PROJECT_ROOT}/output/" "${PIPELINE_DIR}/output/" 2>/dev/null || true

# Create symlink for easy access
ln -sf "${PIPELINE_DIR}" "${COMFYUI_DIR}/ai_pipeline" 2>/dev/null || true

log_info "Pipeline deployed to: ${PIPELINE_DIR}"

# ---------------------------------------------------------------------------
# Step 6: Configure for RTX 5090 / bf16
# ---------------------------------------------------------------------------
log_step "Step 6: GPU Configuration"

# Extra model paths config (so ComfyUI finds models in our directories)
EXTRA_PATHS="${COMFYUI_DIR}/extra_model_paths.yaml"
cat > "${EXTRA_PATHS}" <<YAML_EOF
# AI Influencer Pipeline - Extra Model Paths
# Generated by setup_environment.sh

pipeline:
    base_path: ${MODELS_DIR}
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
YAML_EOF

log_info "Extra model paths configured: ${EXTRA_PATHS}"

# Create startup script
STARTUP_SCRIPT="${COMFYUI_DIR}/start.sh"
cat > "${STARTUP_SCRIPT}" <<'START_EOF'
#!/usr/bin/env bash
# ComfyUI Startup - RTX 5090 Optimized
cd "$(dirname "$0")"

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export CUDA_MODULE_LOADING=LAZY

python3 main.py \
    --listen 0.0.0.0 \
    --port 8188 \
    --bf16-vae \
    --bf16-unet \
    --fast \
    --cuda-malloc \
    --extra-model-paths-config extra_model_paths.yaml \
    "$@"
START_EOF
chmod +x "${STARTUP_SCRIPT}"
log_info "Startup script: ${STARTUP_SCRIPT}"

# ---------------------------------------------------------------------------
# Step 7: Start ComfyUI
# ---------------------------------------------------------------------------
if [[ "$SKIP_START" == false ]]; then
    log_step "Step 7: Starting ComfyUI"

    # Check if already running
    if curl -s "http://localhost:${COMFYUI_PORT}/system_stats" &>/dev/null; then
        log_info "ComfyUI is already running on port ${COMFYUI_PORT}"
    else
        log_info "Starting ComfyUI in background..."
        nohup bash "${STARTUP_SCRIPT}" > "${COMFYUI_DIR}/comfyui.log" 2>&1 &
        COMFY_PID=$!
        log_info "ComfyUI PID: ${COMFY_PID}"

        # Wait for startup
        echo -n "  Waiting for ComfyUI to be ready"
        for i in $(seq 1 30); do
            if curl -s "http://localhost:${COMFYUI_PORT}/system_stats" &>/dev/null; then
                echo -e " ${GREEN}ready!${NC}"
                break
            fi
            echo -n "."
            sleep 2
        done

        if ! curl -s "http://localhost:${COMFYUI_PORT}/system_stats" &>/dev/null; then
            echo -e " ${YELLOW}still loading${NC}"
            log_warn "ComfyUI may still be loading. Check logs: tail -f ${COMFYUI_DIR}/comfyui.log"
        fi
    fi
else
    log_info "Skipping ComfyUI start (--skip-start)"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "============================================================================"
echo -e "${GREEN}  Setup Complete!${NC}"
echo "============================================================================"
echo ""
echo "  ComfyUI:      ${COMFYUI_DIR}"
echo "  Pipeline:     ${PIPELINE_DIR}"
echo "  Models:       ${MODELS_DIR}"
echo "  API:          http://localhost:${COMFYUI_PORT}"
echo "  Logs:         ${COMFYUI_DIR}/comfyui.log"
echo ""
echo "  ┌─────────────────────────────────────────────────────────────┐"
echo "  │  Model Files Required (10 total):                          │"
echo "  │                                                            │"
echo "  │  unet/z_image_bf16.safetensors          Z-Image 6B UNet   │"
echo "  │  clip/qwen_3_4b.safetensors             Qwen CLIP         │"
echo "  │  vae/ultraflux_vae.safetensors          UltraFlux VAE     │"
echo "  │  upscale_models/seedvr2_ema_7b_fp16.safetensors  SeedVR2  │"
echo "  │  vae/ema_vae_fp16.safetensors           SeedVR2 VAE       │"
echo "  │  loras/nicegirls_Zimage.safetensors     Style LoRA 1      │"
echo "  │  loras/Z-TURBO_Photography_*.safetensors Style LoRA 2     │"
echo "  │  loras/psxZStyle_v1_ZIT.safetensors     Style LoRA 3      │"
echo "  │  checkpoints/analogMadnessSDXL_xl5.safetensors  SDXL      │"
echo "  │  ultralytics/YOLOV11m-face.pt           Face Detect       │"
echo "  └─────────────────────────────────────────────────────────────┘"
echo ""
echo "  Quick start:"
echo "    # Generate master prompts for all 21 characters:"
echo "    cd ${PIPELINE_DIR} && python3 scripts/prompt_engine.py master"
echo ""
echo "    # Generate vault manifest (800 images) for a character:"
echo "    python3 scripts/prompt_engine.py vault --char char_001"
echo ""
echo "    # Generate all vault manifests:"
echo "    python3 scripts/prompt_engine.py vault-all"
echo ""
echo "    # Start/restart ComfyUI:"
echo "    bash ${COMFYUI_DIR}/start.sh"
echo ""
echo "============================================================================"
