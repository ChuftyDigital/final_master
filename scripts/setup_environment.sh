#!/usr/bin/env bash
# =============================================================================
# Setup Environment for AI Influencer Image Generation Pipeline
# =============================================================================
#
# This script sets up the complete ComfyUI environment optimised for RTX 5090:
#   1. Pulls the ComfyUI Docker image (comfyui:latest-5090)
#   2. Installs all required custom nodes
#   3. Creates the directory structure
#   4. Downloads required models (placeholder paths for manual download)
#   5. Sets up the Python environment for the orchestrator
#   6. Configures GPU settings for RTX 5090 (32GB VRAM)
#
# Usage:
#   chmod +x setup_environment.sh
#   ./setup_environment.sh [--skip-docker] [--skip-models] [--skip-python]
#
# Requirements:
#   - Docker with NVIDIA Container Toolkit
#   - NVIDIA RTX 5090 with latest drivers (560+)
#   - Python 3.10+
#   - ~100GB free disk space for models
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

DOCKER_IMAGE="comfyui:latest-5090"
COMFYUI_PORT=8188
CONTAINER_NAME="comfyui-influencer-pipeline"

# Colour output helpers
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Colour

log_info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }
log_step()  { echo -e "${BLUE}[STEP]${NC}  $*"; }

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
SKIP_DOCKER=false
SKIP_MODELS=false
SKIP_PYTHON=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --skip-docker) SKIP_DOCKER=true; shift ;;
        --skip-models) SKIP_MODELS=true; shift ;;
        --skip-python) SKIP_PYTHON=true; shift ;;
        -h|--help)
            echo "Usage: $0 [--skip-docker] [--skip-models] [--skip-python]"
            echo ""
            echo "Options:"
            echo "  --skip-docker   Skip Docker image pull and container setup"
            echo "  --skip-models   Skip model download step"
            echo "  --skip-python   Skip Python environment setup"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------
log_step "Running pre-flight checks..."

# Check for NVIDIA GPU
if command -v nvidia-smi &>/dev/null; then
    GPU_NAME=$(nvidia-smi --query-gpu=gpu_name --format=csv,noheader 2>/dev/null | head -1 || echo "unknown")
    GPU_VRAM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1 || echo "0")
    log_info "Detected GPU: ${GPU_NAME} (${GPU_VRAM} MiB VRAM)"

    if [[ "$GPU_VRAM" -lt 30000 ]]; then
        log_warn "This pipeline is optimised for RTX 5090 (32GB). Detected VRAM: ${GPU_VRAM} MiB."
        log_warn "You may need to reduce batch sizes in config/comfyui_settings.json"
    fi
else
    log_warn "nvidia-smi not found. Ensure NVIDIA drivers are installed."
fi

# Check Docker
if ! command -v docker &>/dev/null; then
    log_error "Docker is not installed. Please install Docker first."
    log_error "  https://docs.docker.com/engine/install/"
    exit 1
fi

# Check NVIDIA Container Toolkit
if ! docker info 2>/dev/null | grep -q "nvidia"; then
    log_warn "NVIDIA Container Toolkit may not be installed."
    log_warn "Install: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html"
fi

# Check Python
if ! command -v python3 &>/dev/null; then
    log_error "Python 3 is not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
log_info "Python version: ${PYTHON_VERSION}"

log_info "Pre-flight checks complete."
echo ""

# ---------------------------------------------------------------------------
# Step 1: Create Directory Structure
# ---------------------------------------------------------------------------
log_step "Step 1: Creating directory structure..."

DIRECTORIES=(
    "models/checkpoints"
    "models/loras"
    "models/vae"
    "models/clip"
    "models/controlnet"
    "models/embeddings"
    "models/upscale_models"
    "models/ipadapter"
    "models/insightface"
    "custom_nodes"
    "input"
    "output/master_images"
    "output/lora_datasets"
    "output/lora_models"
    "output/vault"
    "output/temp"
    "output/logs"
    "output/logs/lora_training"
    "workflows"
    "characters"
    "config"
    "scripts"
)

for dir in "${DIRECTORIES[@]}"; do
    mkdir -p "${PROJECT_ROOT}/${dir}"
done

log_info "Directory structure created at: ${PROJECT_ROOT}"
echo ""

# ---------------------------------------------------------------------------
# Step 2: Docker Setup
# ---------------------------------------------------------------------------
if [[ "$SKIP_DOCKER" == false ]]; then
    log_step "Step 2: Setting up Docker environment..."

    # Pull the ComfyUI Docker image
    log_info "Pulling Docker image: ${DOCKER_IMAGE}"
    if docker pull "${DOCKER_IMAGE}" 2>/dev/null; then
        log_info "Docker image pulled successfully."
    else
        log_warn "Could not pull ${DOCKER_IMAGE}. You may need to build it locally."
        log_warn "Attempting to check for local image..."
        if docker image inspect "${DOCKER_IMAGE}" &>/dev/null; then
            log_info "Local image found: ${DOCKER_IMAGE}"
        else
            log_warn "Image not found locally either. You will need to build or pull it manually."
            log_warn "  docker build -t ${DOCKER_IMAGE} ."
        fi
    fi

    # Stop existing container if running
    if docker ps -q -f "name=${CONTAINER_NAME}" | grep -q .; then
        log_info "Stopping existing container: ${CONTAINER_NAME}"
        docker stop "${CONTAINER_NAME}" 2>/dev/null || true
        docker rm "${CONTAINER_NAME}" 2>/dev/null || true
    fi

    # Create docker-compose.yml for convenience
    COMPOSE_FILE="${PROJECT_ROOT}/docker-compose.yml"
    cat > "${COMPOSE_FILE}" <<'COMPOSE_EOF'
version: "3.9"

services:
  comfyui:
    image: comfyui:latest-5090
    container_name: comfyui-influencer-pipeline
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=0
      - CUDA_VISIBLE_DEVICES=0
    ports:
      - "8188:8188"
    volumes:
      - ./models:/comfyui/models
      - ./output:/comfyui/output
      - ./input:/comfyui/input
      - ./custom_nodes:/comfyui/custom_nodes
      - ./workflows:/comfyui/workflows
    shm_size: "16g"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    command: >
      python main.py
        --listen 0.0.0.0
        --port 8188
        --bf16-vae
        --bf16-unet
        --fast
        --cuda-malloc
    restart: unless-stopped
COMPOSE_EOF

    log_info "docker-compose.yml created at: ${COMPOSE_FILE}"
    log_info "Start with: cd ${PROJECT_ROOT} && docker-compose up -d"
    echo ""
else
    log_info "Skipping Docker setup (--skip-docker)"
    echo ""
fi

# ---------------------------------------------------------------------------
# Step 3: Install Custom Nodes
# ---------------------------------------------------------------------------
log_step "Step 3: Installing custom nodes..."

CUSTOM_NODES_DIR="${PROJECT_ROOT}/custom_nodes"

declare -A CUSTOM_NODES=(
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

for node_name in "${!CUSTOM_NODES[@]}"; do
    node_dir="${CUSTOM_NODES_DIR}/${node_name}"
    repo_url="${CUSTOM_NODES[${node_name}]}"

    if [[ -d "$node_dir" ]]; then
        log_info "  Updating: ${node_name}"
        (cd "$node_dir" && git pull --quiet 2>/dev/null) || log_warn "  Could not update ${node_name}"
    else
        log_info "  Cloning: ${node_name}"
        git clone --quiet "$repo_url" "$node_dir" 2>/dev/null || {
            log_warn "  Could not clone ${node_name} from ${repo_url}"
            log_warn "  You may need to install it manually via ComfyUI Manager"
        }
    fi

    # Install node dependencies if requirements.txt exists
    if [[ -f "${node_dir}/requirements.txt" ]]; then
        pip install -q -r "${node_dir}/requirements.txt" 2>/dev/null || true
    fi
done

log_info "Custom nodes installed to: ${CUSTOM_NODES_DIR}"
echo ""

# ---------------------------------------------------------------------------
# Step 4: Download Models (Placeholder)
# ---------------------------------------------------------------------------
if [[ "$SKIP_MODELS" == false ]]; then
    log_step "Step 4: Model download setup..."

    MODELS_DIR="${PROJECT_ROOT}/models"

    log_warn "Models must be downloaded manually due to license requirements."
    log_warn "Place them in the following locations:"
    echo ""
    echo "  CHECKPOINTS (${MODELS_DIR}/checkpoints/):"
    echo "    - juggernautXL_v9.safetensors"
    echo "      Source: https://civitai.com/models/133005/juggernaut-xl"
    echo ""
    echo "  VAE (${MODELS_DIR}/vae/):"
    echo "    - sdxl_vae.safetensors"
    echo "      Source: https://huggingface.co/stabilityai/sdxl-vae"
    echo ""
    echo "  EMBEDDINGS (${MODELS_DIR}/embeddings/):"
    echo "    - negativeXL_D.safetensors"
    echo "      Source: https://civitai.com/models/118418"
    echo ""
    echo "  IP-ADAPTER (${MODELS_DIR}/ipadapter/):"
    echo "    - ip-adapter-plus_sdxl_vit-h.safetensors"
    echo "      Source: https://huggingface.co/h94/IP-Adapter"
    echo ""
    echo "  CLIP VISION (${MODELS_DIR}/clip/):"
    echo "    - clip_vision_g.safetensors"
    echo "      Source: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0"
    echo ""
    echo "  UPSCALE (${MODELS_DIR}/upscale_models/):"
    echo "    - 4x-UltraSharp.pth"
    echo "      Source: https://openmodeldb.info/models/4x-UltraSharp"
    echo ""

    # Create a download helper script
    DOWNLOAD_SCRIPT="${MODELS_DIR}/download_models.sh"
    cat > "${DOWNLOAD_SCRIPT}" <<'DL_EOF'
#!/usr/bin/env bash
# Model Download Helper
# Uncomment and modify URLs as needed. Many models require CivitAI API key.

MODELS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Downloading models to: ${MODELS_DIR}"
echo "Note: Some downloads require API keys or manual browser download."
echo ""

# Example with huggingface-cli (install: pip install huggingface_hub)
# huggingface-cli download stabilityai/sdxl-vae --local-dir "${MODELS_DIR}/vae/"

# Example with wget
# wget -O "${MODELS_DIR}/checkpoints/juggernautXL_v9.safetensors" "YOUR_DOWNLOAD_URL_HERE"

echo "Please download models manually and place them in the correct directories."
echo "See setup_environment.sh output for required models and sources."
DL_EOF
    chmod +x "${DOWNLOAD_SCRIPT}"

    log_info "Download helper script created: ${DOWNLOAD_SCRIPT}"
    echo ""
else
    log_info "Skipping model download (--skip-models)"
    echo ""
fi

# ---------------------------------------------------------------------------
# Step 5: Python Environment Setup
# ---------------------------------------------------------------------------
if [[ "$SKIP_PYTHON" == false ]]; then
    log_step "Step 5: Setting up Python environment..."

    VENV_DIR="${PROJECT_ROOT}/.venv"

    # Create virtual environment if it does not exist
    if [[ ! -d "$VENV_DIR" ]]; then
        log_info "Creating virtual environment at: ${VENV_DIR}"
        python3 -m venv "$VENV_DIR"
    else
        log_info "Virtual environment already exists: ${VENV_DIR}"
    fi

    # Activate and install dependencies
    source "${VENV_DIR}/bin/activate"

    log_info "Installing Python dependencies..."

    pip install --upgrade pip setuptools wheel -q

    # Core orchestrator dependencies
    pip install -q \
        requests>=2.31.0 \
        websocket-client>=1.7.0 \
        Pillow>=10.0.0 \
        tqdm>=4.66.0 \
        toml>=0.10.2 \
        pyyaml>=6.0

    # LoRA training dependencies (kohya_ss compatible)
    pip install -q \
        torch>=2.2.0 \
        torchvision>=0.17.0 \
        accelerate>=0.27.0 \
        transformers>=4.38.0 \
        safetensors>=0.4.0 \
        prodigyopt>=1.0

    log_info "Python dependencies installed."

    # Create a requirements.txt for reproducibility
    REQUIREMENTS_FILE="${PROJECT_ROOT}/requirements.txt"
    cat > "${REQUIREMENTS_FILE}" <<'REQ_EOF'
# AI Influencer Pipeline - Python Dependencies
# Install: pip install -r requirements.txt

# Core orchestrator
requests>=2.31.0
websocket-client>=1.7.0
Pillow>=10.0.0
tqdm>=4.66.0
toml>=0.10.2
pyyaml>=6.0

# LoRA training (kohya_ss)
torch>=2.2.0
torchvision>=0.17.0
accelerate>=0.27.0
transformers>=4.38.0
safetensors>=0.4.0
prodigyopt>=1.0

# Optional: development
# black
# ruff
# pytest
REQ_EOF

    log_info "requirements.txt created at: ${REQUIREMENTS_FILE}"
    echo ""
else
    log_info "Skipping Python environment setup (--skip-python)"
    echo ""
fi

# ---------------------------------------------------------------------------
# Step 6: RTX 5090 Configuration
# ---------------------------------------------------------------------------
log_step "Step 6: Configuring for RTX 5090..."

# Set optimal CUDA environment variables
ENV_FILE="${PROJECT_ROOT}/.env"
cat > "${ENV_FILE}" <<'ENV_EOF'
# RTX 5090 Optimisation Environment Variables
# Source this file or use with docker-compose

# CUDA Configuration
NVIDIA_VISIBLE_DEVICES=0
CUDA_VISIBLE_DEVICES=0
CUDA_LAUNCH_BLOCKING=0
TORCH_CUDA_ARCH_LIST="12.0"

# Memory optimisation
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
CUDA_MODULE_LOADING=LAZY

# ComfyUI specific
COMFYUI_EXTRA_ARGS=--bf16-vae --bf16-unet --fast --cuda-malloc

# Kohya_ss / training
ACCELERATE_MIXED_PRECISION=bf16
ENV_EOF

log_info "Environment file created: ${ENV_FILE}"
echo ""

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "============================================================================"
echo -e "${GREEN}  Setup Complete!${NC}"
echo "============================================================================"
echo ""
echo "  Project root:     ${PROJECT_ROOT}"
echo "  Docker image:     ${DOCKER_IMAGE}"
echo "  Python venv:      ${PROJECT_ROOT}/.venv"
echo "  ComfyUI port:     ${COMFYUI_PORT}"
echo ""
echo "  Next steps:"
echo "    1. Download required models (see Step 4 output above)"
echo "    2. Start ComfyUI:"
echo "         cd ${PROJECT_ROOT} && docker-compose up -d"
echo "    3. Verify ComfyUI is running:"
echo "         curl http://localhost:${COMFYUI_PORT}/system_stats"
echo "    4. Activate Python environment:"
echo "         source ${PROJECT_ROOT}/.venv/bin/activate"
echo "    5. Run the pipeline:"
echo "         python scripts/orchestrator.py full-pipeline"
echo ""
echo "  For single character:"
echo "    python scripts/orchestrator.py generate-masters --character aria_nova"
echo ""
echo "============================================================================"
