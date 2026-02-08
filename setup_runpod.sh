#!/bin/bash
# Super Factory Ultimate - RunPod RTX 5090 One-Shot Setup
# Run this once when your pod starts. Everything else is handled by main.py.
#
# Usage:
#   bash setup_runpod.sh
#
# What it does:
#   1. Verifies GPU (RTX 5090 / Blackwell)
#   2. Installs PyTorch nightly with CUDA 12.8
#   3. Installs ComfyUI + custom nodes
#   4. Downloads all AI models (~30GB)
#   5. Clones this project to /workspace/superfactory
#   6. Creates optimized ComfyUI launch script
#
# After setup, use:
#   cd /workspace/superfactory
#   python main.py status
#   python main.py references
#   python main.py generate

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

COMFYUI_DIR="/workspace/ComfyUI"
PROJECT_DIR="/workspace/superfactory"

echo "========================================"
echo " Super Factory Ultimate - RTX 5090 Setup"
echo "========================================"
echo ""

# ── Step 1: GPU Check ────────────────────────────────────────────────────
echo -e "${YELLOW}[1/7] Checking GPU...${NC}"
nvidia-smi
GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo "unknown")
GPU_MEM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null || echo "0")
echo -e "${GREEN}GPU: $GPU_NAME (${GPU_MEM}MB VRAM)${NC}"
echo ""

# ── Step 2: PyTorch with CUDA 12.8 ───────────────────────────────────────
echo -e "${YELLOW}[2/7] Checking PyTorch / CUDA 12.8...${NC}"
CUDA_VER=$(python3 -c "import torch; print(torch.version.cuda or '')" 2>/dev/null || echo "")
if [[ "$CUDA_VER" == 12.8* ]]; then
    echo -e "${GREEN}PyTorch already has CUDA $CUDA_VER - skipping install${NC}"
else
    echo "Installing PyTorch nightly with CUDA 12.8..."
    python3 -m pip install --upgrade pip -q
    python3 -m pip uninstall -y torch torchvision torchaudio 2>/dev/null || true
    python3 -m pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128 -q
fi

# Verify
python3 -c "
import torch
print(f'PyTorch: {torch.__version__}')
print(f'CUDA: {torch.version.cuda}')
if torch.cuda.is_available():
    print(f'Device: {torch.cuda.get_device_name(0)}')
    print(f'VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB')
else:
    print('WARNING: CUDA not available')
"
echo -e "${GREEN}PyTorch installed${NC}"
echo ""

# ── Step 3: Install Triton for Blackwell ──────────────────────────────────
echo -e "${YELLOW}[3/7] Installing Triton (Blackwell support)...${NC}"
python3 -m pip install -U --pre triton -q
echo -e "${GREEN}Triton installed${NC}"
echo ""

# ── Step 4: ComfyUI ──────────────────────────────────────────────────────
echo -e "${YELLOW}[4/7] Setting up ComfyUI...${NC}"
if [ ! -d "$COMFYUI_DIR" ]; then
    git clone https://github.com/comfyanonymous/ComfyUI.git "$COMFYUI_DIR"
fi
cd "$COMFYUI_DIR"
git pull -q
python3 -m pip install -r requirements.txt -q
echo -e "${GREEN}ComfyUI ready${NC}"
echo ""

# ── Step 5: Custom Nodes ─────────────────────────────────────────────────
echo -e "${YELLOW}[5/7] Installing custom nodes...${NC}"
mkdir -p "$COMFYUI_DIR/custom_nodes"
cd "$COMFYUI_DIR/custom_nodes"

install_node() {
    local name=$1
    local url=$2
    local has_reqs=$3
    if [ ! -d "$name" ]; then
        echo "  Cloning $name..."
        git clone --depth 1 "$url" "$name" -q
    else
        echo "  Updating $name..."
        cd "$name" && git pull -q && cd ..
    fi
    if [ "$has_reqs" = "true" ] && [ -f "$name/requirements.txt" ]; then
        python3 -m pip install -r "$name/requirements.txt" -q 2>/dev/null || true
    fi
}

install_node "ComfyUI-Manager" "https://github.com/ltdrdata/ComfyUI-Manager.git" "true"
install_node "ComfyUI_IPAdapter_plus" "https://github.com/cubiq/ComfyUI_IPAdapter_plus.git" "false"
install_node "ComfyUI_InstantID" "https://github.com/cubiq/ComfyUI_InstantID.git" "false"
install_node "ComfyUI-Impact-Pack" "https://github.com/ltdrdata/ComfyUI-Impact-Pack.git" "true"
install_node "comfyui_controlnet_aux" "https://github.com/Fannovel16/comfyui_controlnet_aux.git" "true"

echo -e "${GREEN}Custom nodes installed${NC}"
echo ""

# ── Step 6: Project Setup ────────────────────────────────────────────────
echo -e "${YELLOW}[6/7] Setting up Super Factory...${NC}"
if [ ! -d "$PROJECT_DIR" ]; then
    # Copy from current location or clone
    if [ -f "$(dirname "$0")/main.py" ]; then
        cp -r "$(dirname "$0")" "$PROJECT_DIR"
    else
        echo "  Please copy the project to $PROJECT_DIR"
    fi
fi

cd "$PROJECT_DIR"
python3 -m pip install -r requirements.txt -q
echo -e "${GREEN}Project ready at $PROJECT_DIR${NC}"
echo ""

# ── Step 7: Download Models ──────────────────────────────────────────────
echo -e "${YELLOW}[7/7] Downloading AI models (~30GB, this takes a while)...${NC}"
cd "$PROJECT_DIR"
python3 main.py install --comfyui-path "$COMFYUI_DIR" 2>&1 || echo -e "${YELLOW}Some models may need retry${NC}"
echo ""

# ── Create Launch Script ─────────────────────────────────────────────────
cat > "$COMFYUI_DIR/start.sh" << 'LAUNCH'
#!/bin/bash
cd "$(dirname "$0")"
echo "Starting ComfyUI (RTX 5090 Blackwell optimized)..."
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF="max_split_size_mb:512"

python main.py \
    --listen 0.0.0.0 \
    --port 8188 \
    --highvram \
    --fp8_e4m3fn-unet \
    --fp8_e5m2-unet \
    --bf16-unet \
    --disable-xformers \
    "$@"
LAUNCH
chmod +x "$COMFYUI_DIR/start.sh"

# ── Done ──────────────────────────────────────────────────────────────────
echo ""
echo "========================================"
echo -e "${GREEN}SETUP COMPLETE!${NC}"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "  1. Start ComfyUI:"
echo "     cd $COMFYUI_DIR && ./start.sh"
echo ""
echo "  2. Check status:"
echo "     cd $PROJECT_DIR && python main.py status"
echo ""
echo "  3. Generate reference images:"
echo "     python main.py references"
echo ""
echo "  4. Test with small batch:"
echo "     python main.py generate --character 1 --lanes sfw --count 5"
echo ""
echo "  5. Full production run (16,800 images):"
echo "     python main.py generate"
echo ""
echo "  ComfyUI Web UI: http://your-pod-ip:8188"
echo "========================================"
