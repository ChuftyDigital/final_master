"""Model and custom node installer for ComfyUI."""

import json
import logging
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger("superfactory.installer")

# All required models with verified HuggingFace URLs
MODELS = [
    {
        "name": "Z-Image Base (BF16)",
        "url": "https://huggingface.co/Comfy-Org/z_image/resolve/main/split_files/diffusion_models/z_image_bf16.safetensors",
        "subdir": "checkpoints",
        "filename": "z_image_bf16.safetensors",
        "size_gb": 12.3,
        "category": "core",
    },
    {
        "name": "Z-Image Turbo (BF16)",
        "url": "https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors",
        "subdir": "checkpoints",
        "filename": "z_image_turbo_bf16.safetensors",
        "size_gb": 12.3,
        "category": "core",
    },
    {
        "name": "CLIP Vision (ViT-H)",
        "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/models/image_encoder/model.safetensors",
        "subdir": "clip_vision",
        "filename": "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors",
        "size_gb": 2.4,
        "category": "clip",
    },
    {
        "name": "IPAdapter Plus SD1.5",
        "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus_sd15.bin",
        "subdir": "ipadapter",
        "filename": "ip-adapter-plus_sd15.bin",
        "size_gb": 0.15,
        "category": "ipadapter",
    },
    {
        "name": "IPAdapter Plus SDXL",
        "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.bin",
        "subdir": "ipadapter",
        "filename": "ip-adapter-plus_sdxl_vit-h.bin",
        "size_gb": 0.97,
        "category": "ipadapter",
    },
    {
        "name": "InstantID Adapter",
        "url": "https://huggingface.co/InstantX/InstantID/resolve/main/ip-adapter.bin",
        "subdir": "instantid",
        "filename": "ip-adapter.bin",
        "size_gb": 1.6,
        "category": "instantid",
    },
    {
        "name": "InstantID ControlNet",
        "url": "https://huggingface.co/InstantX/InstantID/resolve/main/ControlNetModel/diffusion_pytorch_model.safetensors",
        "subdir": "controlnet",
        "filename": "diffusion_pytorch_model.safetensors",
        "size_gb": 2.4,
        "category": "instantid",
    },
    {
        "name": "OpenPose ControlNet",
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth",
        "subdir": "controlnet",
        "filename": "control_v11p_sd15_openpose.pth",
        "size_gb": 1.4,
        "category": "controlnet",
    },
    {
        "name": "4x ClearReality Upscaler",
        "url": "https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/4x-ClearRealityV1.pth",
        "subdir": "upscale_models",
        "filename": "4x-ClearRealityV1.pth",
        "size_gb": 0.06,
        "category": "upscale",
    },
    {
        "name": "YOLO Face Detection",
        "url": "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8m.pt",
        "subdir": "ultralytics/bbox",
        "filename": "face_yolov8m.pt",
        "size_gb": 0.05,
        "category": "detection",
    },
    {
        "name": "SAM Segmentation",
        "url": "https://huggingface.co/daswerth/sd-webui-segment-anything/resolve/main/sam_vit_b_01ec64.pth",
        "subdir": "sams",
        "filename": "sam_vit_b_01ec64.pth",
        "size_gb": 0.37,
        "category": "detection",
    },
    {
        "name": "VAE (ae.safetensors)",
        "url": "https://huggingface.co/Comfy-Org/z_image/resolve/main/split_files/vae/ae.safetensors",
        "subdir": "vae",
        "filename": "ae.safetensors",
        "size_gb": 0.17,
        "category": "core",
    },
]

CUSTOM_NODES = [
    {"name": "ComfyUI-Manager", "url": "https://github.com/ltdrdata/ComfyUI-Manager.git", "requirements": True},
    {"name": "ComfyUI_IPAdapter_plus", "url": "https://github.com/cubiq/ComfyUI_IPAdapter_plus.git", "requirements": False},
    {"name": "ComfyUI_InstantID", "url": "https://github.com/cubiq/ComfyUI_InstantID.git", "requirements": False},
    {"name": "ComfyUI-Impact-Pack", "url": "https://github.com/ltdrdata/ComfyUI-Impact-Pack.git", "requirements": True},
    {"name": "comfyui_controlnet_aux", "url": "https://github.com/Fannovel16/comfyui_controlnet_aux.git", "requirements": True},
]


class ModelInstaller:
    """Downloads all required models and installs custom nodes."""

    def __init__(self, comfyui_path: str):
        self.comfyui_path = Path(comfyui_path)
        self.models_dir = self.comfyui_path / "models"
        self.nodes_dir = self.comfyui_path / "custom_nodes"
        self._state_file = self.comfyui_path / ".superfactory_install_state.json"

    def _load_state(self) -> Dict:
        if self._state_file.exists():
            with open(self._state_file) as f:
                return json.load(f)
        return {"models": [], "nodes": [], "failed": []}

    def _save_state(self, state: Dict):
        with open(self._state_file, "w") as f:
            json.dump(state, f, indent=2)

    def _create_dirs(self):
        """Create all required model directories."""
        for model in MODELS:
            (self.models_dir / model["subdir"]).mkdir(parents=True, exist_ok=True)
        self.nodes_dir.mkdir(parents=True, exist_ok=True)

    def _verify_model(self, model: Dict) -> bool:
        """Check if a model file exists and has reasonable size."""
        path = self.models_dir / model["subdir"] / model["filename"]
        return path.exists() and path.stat().st_size > 1_000_000  # >1MB

    def _download(self, url: str, dest: Path, max_retries: int = 3) -> bool:
        """Download a file with retry logic using wget or curl."""
        for attempt in range(1, max_retries + 1):
            # Try wget first
            try:
                result = subprocess.run(
                    ["wget", "--progress=bar:force", "--timeout=300", "--tries=2", "-O", str(dest), url],
                    capture_output=True, text=True, timeout=3600,
                )
                if result.returncode == 0 and dest.exists() and dest.stat().st_size > 1_000_000:
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

            # Fall back to curl
            try:
                if dest.exists():
                    dest.unlink()
                result = subprocess.run(
                    ["curl", "-L", "--max-time", "3600", "--retry", "2", "--progress-bar", "-o", str(dest), url],
                    capture_output=True, text=True, timeout=3600,
                )
                if result.returncode == 0 and dest.exists() and dest.stat().st_size > 1_000_000:
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

            if attempt < max_retries:
                wait = 5 * attempt
                logger.info(f"  Retry {attempt}/{max_retries} in {wait}s...")
                time.sleep(wait)
                if dest.exists():
                    dest.unlink()

        return False

    def install_models(self, categories: Optional[List[str]] = None) -> Dict[str, bool]:
        """Download all models (or filtered by category)."""
        self._create_dirs()
        state = self._load_state()
        results = {}

        models = MODELS
        if categories:
            models = [m for m in MODELS if m["category"] in categories]

        total_gb = sum(m["size_gb"] for m in models)
        logger.info(f"Installing {len(models)} models (~{total_gb:.1f} GB)")

        for i, model in enumerate(models, 1):
            name = model["name"]

            if name in state["models"] and self._verify_model(model):
                logger.info(f"  [{i}/{len(models)}] {name} - already installed")
                results[name] = True
                continue

            logger.info(f"  [{i}/{len(models)}] {name} ({model['size_gb']:.1f} GB)")
            dest = self.models_dir / model["subdir"] / model["filename"]

            if self._download(model["url"], dest):
                size_mb = dest.stat().st_size / (1024 * 1024)
                logger.info(f"    OK ({size_mb:.0f} MB)")
                state["models"].append(name)
                results[name] = True
            else:
                logger.error(f"    FAILED")
                state["failed"].append(name)
                results[name] = False

            self._save_state(state)

        return results

    def install_nodes(self) -> Dict[str, bool]:
        """Install all required custom nodes."""
        self._create_dirs()
        state = self._load_state()
        results = {}

        for i, node in enumerate(CUSTOM_NODES, 1):
            name = node["name"]

            if name in state["nodes"]:
                logger.info(f"  [{i}/{len(CUSTOM_NODES)}] {name} - already installed")
                results[name] = True
                continue

            node_dir = self.nodes_dir / name
            logger.info(f"  [{i}/{len(CUSTOM_NODES)}] Installing {name}")

            try:
                if node_dir.exists():
                    subprocess.run(["git", "pull"], cwd=str(node_dir), capture_output=True, timeout=60)
                else:
                    subprocess.run(
                        ["git", "clone", "--depth", "1", node["url"], name],
                        cwd=str(self.nodes_dir), capture_output=True, timeout=120,
                    )

                if node.get("requirements"):
                    req = node_dir / "requirements.txt"
                    if req.exists():
                        subprocess.run(
                            [sys.executable, "-m", "pip", "install", "-q", "-r", str(req)],
                            capture_output=True, timeout=300,
                        )

                state["nodes"].append(name)
                results[name] = True
                logger.info(f"    OK")
            except Exception as e:
                logger.error(f"    FAILED: {e}")
                results[name] = False

            self._save_state(state)

        return results

    def install_all(self) -> bool:
        """Run complete installation of models and nodes."""
        logger.info("=" * 70)
        logger.info("SUPER FACTORY - MODEL INSTALLER")
        logger.info(f"ComfyUI: {self.comfyui_path}")
        logger.info("=" * 70)

        model_results = self.install_models()
        node_results = self.install_nodes()

        failed = [k for k, v in {**model_results, **node_results}.items() if not v]
        if failed:
            logger.warning(f"\n{len(failed)} items failed: {', '.join(failed)}")
            logger.info("Run the installer again to retry failed items.")
            return False

        logger.info("\nAll models and nodes installed successfully!")
        return True

    def status(self):
        """Print current installation status."""
        logger.info("Model Status:")
        for model in MODELS:
            installed = self._verify_model(model)
            status = "OK" if installed else "MISSING"
            logger.info(f"  [{status:7s}] {model['name']}")

        logger.info("\nCustom Node Status:")
        for node in CUSTOM_NODES:
            installed = (self.nodes_dir / node["name"]).exists()
            status = "OK" if installed else "MISSING"
            logger.info(f"  [{status:7s}] {node['name']}")
