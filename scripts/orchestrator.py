#!/usr/bin/env python3
"""
Master Orchestrator for AI Influencer Image Generation Pipeline
===============================================================

Coordinates the entire image generation pipeline across three phases:
  Phase 1: Master image generation via ComfyUI Workflow 1
  Phase 2: LoRA training preparation for kohya_ss
  Phase 3: Vault content generation via ComfyUI Workflow 2 with trained LoRAs

Optimized for NVIDIA RTX 5090 (32GB VRAM) with bf16 precision and large batch sizes.

Usage:
    python orchestrator.py generate-masters [--character SLUG]
    python orchestrator.py prepare-lora [--character SLUG]
    python orchestrator.py generate-vault [--character SLUG]
    python orchestrator.py full-pipeline [--character SLUG]

Dependencies:
    - ComfyUI running (Docker or local) with API access
    - characters/personas.json character database
    - scripts/prompt_engine.py prompt generation module
"""

import argparse
import json
import logging
import os
import sys
import time
import uuid
import shutil
import subprocess
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin

import requests
import websocket

# ---------------------------------------------------------------------------
# Path setup -- resolve project root relative to this script
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(PROJECT_ROOT))

# Local imports -- prompt_engine lives in scripts/
from prompt_engine import PromptEngine  # noqa: E402

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("orchestrator")

# ---------------------------------------------------------------------------
# Constants & defaults
# ---------------------------------------------------------------------------
DEFAULT_COMFYUI_HOST = "127.0.0.1"
DEFAULT_COMFYUI_PORT = 8188
DEFAULT_CLIENT_ID = str(uuid.uuid4())

PERSONAS_PATH = PROJECT_ROOT / "characters" / "personas.json"
COMFYUI_SETTINGS_PATH = PROJECT_ROOT / "config" / "comfyui_settings.json"
LORA_CONFIG_PATH = PROJECT_ROOT / "config" / "lora_training_config.json"

MASTER_IMAGES_DIR = PROJECT_ROOT / "output" / "master_images"
LORA_DATASETS_DIR = PROJECT_ROOT / "output" / "lora_datasets"
LORA_MODELS_DIR = PROJECT_ROOT / "output" / "lora_models"
VAULT_OUTPUT_DIR = PROJECT_ROOT / "output" / "vault"

# RTX 5090 optimised defaults
RTX5090_VRAM_GB = 32
DEFAULT_PRECISION = "bf16"
DEFAULT_BATCH_SIZE = 4  # larger batch thanks to 32 GB VRAM

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5
POLL_INTERVAL_SECONDS = 2


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
class PipelinePhase(Enum):
    MASTER_GEN = "generate-masters"
    LORA_PREP = "prepare-lora"
    VAULT_GEN = "generate-vault"


@dataclass
class GenerationJob:
    """Tracks a single image generation job submitted to ComfyUI."""
    prompt_id: str
    character_slug: str
    phase: PipelinePhase
    status: str = "queued"  # queued | running | completed | failed
    attempts: int = 0
    output_files: List[str] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class ProgressTracker:
    """Aggregate progress across all jobs in a pipeline run."""
    total: int = 0
    completed: int = 0
    failed: int = 0
    jobs: List[GenerationJob] = field(default_factory=list)

    @property
    def pending(self) -> int:
        return self.total - self.completed - self.failed

    def summary(self) -> str:
        return (
            f"Progress: {self.completed}/{self.total} completed, "
            f"{self.failed} failed, {self.pending} pending"
        )


# ---------------------------------------------------------------------------
# ComfyUI API Client
# ---------------------------------------------------------------------------
class ComfyUIClient:
    """
    Client for the ComfyUI HTTP + WebSocket API.

    Capabilities:
        - Queue prompt workflows
        - Poll / stream job status via WebSocket
        - Download generated images
        - Check system info and GPU memory
    """

    def __init__(
        self,
        host: str = DEFAULT_COMFYUI_HOST,
        port: int = DEFAULT_COMFYUI_PORT,
        client_id: Optional[str] = None,
    ):
        self.host = host
        self.port = port
        self.client_id = client_id or DEFAULT_CLIENT_ID
        self.base_url = f"http://{self.host}:{self.port}"
        self.ws_url = f"ws://{self.host}:{self.port}/ws?clientId={self.client_id}"
        self._session = requests.Session()

    # -- low-level helpers ---------------------------------------------------

    def _get(self, path: str, **kwargs) -> requests.Response:
        url = urljoin(self.base_url + "/", path.lstrip("/"))
        resp = self._session.get(url, **kwargs)
        resp.raise_for_status()
        return resp

    def _post(self, path: str, json_data: Any = None, **kwargs) -> requests.Response:
        url = urljoin(self.base_url + "/", path.lstrip("/"))
        resp = self._session.post(url, json=json_data, **kwargs)
        resp.raise_for_status()
        return resp

    # -- system --------------------------------------------------------------

    def get_system_stats(self) -> Dict:
        """Return ComfyUI system stats including GPU memory info."""
        return self._get("/system_stats").json()

    def check_gpu_memory(self) -> Dict:
        """Return current VRAM usage from ComfyUI system stats."""
        stats = self.get_system_stats()
        devices = stats.get("devices", [])
        if devices:
            dev = devices[0]
            return {
                "name": dev.get("name", "unknown"),
                "vram_total_gb": round(dev.get("vram_total", 0) / 1e9, 2),
                "vram_free_gb": round(dev.get("vram_free", 0) / 1e9, 2),
                "torch_vram_total_gb": round(dev.get("torch_vram_total", 0) / 1e9, 2),
                "torch_vram_free_gb": round(dev.get("torch_vram_free", 0) / 1e9, 2),
            }
        return {}

    def is_alive(self) -> bool:
        """Return True if the ComfyUI server is reachable."""
        try:
            self._get("/system_stats")
            return True
        except Exception:
            return False

    # -- prompt queue --------------------------------------------------------

    def queue_prompt(self, workflow: Dict, extra_data: Optional[Dict] = None) -> str:
        """
        Submit a workflow (prompt) to the ComfyUI queue.

        Parameters
        ----------
        workflow : dict
            The full ComfyUI workflow/prompt JSON.
        extra_data : dict, optional
            Extra payload fields (e.g. ``extra_pnginfo``).

        Returns
        -------
        str
            The ``prompt_id`` assigned by ComfyUI.
        """
        payload: Dict[str, Any] = {
            "prompt": workflow,
            "client_id": self.client_id,
        }
        if extra_data:
            payload["extra_data"] = extra_data
        resp = self._post("/prompt", json_data=payload)
        data = resp.json()
        prompt_id = data.get("prompt_id")
        if not prompt_id:
            raise RuntimeError(f"ComfyUI did not return a prompt_id: {data}")
        logger.info("Queued prompt %s", prompt_id)
        return prompt_id

    def get_queue(self) -> Dict:
        """Return the current ComfyUI queue state."""
        return self._get("/queue").json()

    def get_history(self, prompt_id: str) -> Dict:
        """Return execution history for a given prompt_id."""
        return self._get(f"/history/{prompt_id}").json()

    def get_prompt_status(self, prompt_id: str) -> str:
        """
        Determine the status of a queued prompt.

        Returns one of: ``queued``, ``running``, ``completed``, ``failed``.
        """
        queue = self.get_queue()

        # Check running queue
        for item in queue.get("queue_running", []):
            if item[1] == prompt_id:
                return "running"

        # Check pending queue
        for item in queue.get("queue_pending", []):
            if item[1] == prompt_id:
                return "queued"

        # If not in queue, check history
        history = self.get_history(prompt_id)
        if prompt_id in history:
            entry = history[prompt_id]
            status_obj = entry.get("status", {})
            if status_obj.get("completed", False):
                return "completed"
            if status_obj.get("status_str") == "error":
                return "failed"
            # Outputs present means completed
            if entry.get("outputs"):
                return "completed"
            return "failed"

        return "queued"  # not yet picked up

    def wait_for_completion(
        self,
        prompt_id: str,
        timeout: int = 600,
        poll_interval: float = POLL_INTERVAL_SECONDS,
    ) -> str:
        """
        Block until *prompt_id* finishes (completed / failed) or *timeout* is hit.

        Returns the final status string.
        """
        logger.info("Waiting for prompt %s (timeout=%ds)...", prompt_id, timeout)
        deadline = time.time() + timeout
        while time.time() < deadline:
            status = self.get_prompt_status(prompt_id)
            if status in ("completed", "failed"):
                logger.info("Prompt %s finished with status: %s", prompt_id, status)
                return status
            time.sleep(poll_interval)
        raise TimeoutError(
            f"Prompt {prompt_id} did not complete within {timeout}s"
        )

    def wait_for_completion_ws(self, prompt_id: str, timeout: int = 600) -> str:
        """
        Wait for completion using WebSocket streaming (lower latency).

        Falls back to polling if the WebSocket connection fails.
        """
        try:
            ws = websocket.create_connection(
                self.ws_url, timeout=timeout
            )
        except Exception as exc:
            logger.warning(
                "WebSocket connection failed (%s); falling back to polling.", exc
            )
            return self.wait_for_completion(prompt_id, timeout=timeout)

        try:
            deadline = time.time() + timeout
            while time.time() < deadline:
                ws.settimeout(max(1, deadline - time.time()))
                try:
                    raw = ws.recv()
                except websocket.WebSocketTimeoutException:
                    continue
                if not raw:
                    continue
                msg = json.loads(raw)
                msg_type = msg.get("type")
                data = msg.get("data", {})
                if msg_type == "executed" and data.get("prompt_id") == prompt_id:
                    return "completed"
                if msg_type == "execution_error" and data.get("prompt_id") == prompt_id:
                    return "failed"
            raise TimeoutError(
                f"Prompt {prompt_id} did not complete within {timeout}s (ws)"
            )
        finally:
            ws.close()

    # -- output retrieval ----------------------------------------------------

    def get_output_images(self, prompt_id: str) -> List[Dict]:
        """
        Retrieve output image metadata for a completed prompt.

        Returns a list of dicts with keys: ``filename``, ``subfolder``, ``type``.
        """
        history = self.get_history(prompt_id)
        entry = history.get(prompt_id, {})
        outputs = entry.get("outputs", {})
        images: List[Dict] = []
        for _node_id, node_out in outputs.items():
            for img in node_out.get("images", []):
                images.append(img)
        return images

    def download_image(
        self,
        filename: str,
        subfolder: str = "",
        img_type: str = "output",
        dest_path: Optional[Path] = None,
    ) -> Path:
        """
        Download an image from ComfyUI to *dest_path*.

        If *dest_path* is ``None`` the file is saved to the current directory.
        """
        params = {
            "filename": filename,
            "subfolder": subfolder,
            "type": img_type,
        }
        resp = self._get("/view", params=params)
        if dest_path is None:
            dest_path = Path(filename)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_bytes(resp.content)
        logger.info("Downloaded %s -> %s", filename, dest_path)
        return dest_path

    def download_prompt_outputs(
        self, prompt_id: str, dest_dir: Path
    ) -> List[Path]:
        """Download all output images for *prompt_id* into *dest_dir*."""
        images = self.get_output_images(prompt_id)
        paths: List[Path] = []
        for img in images:
            dest = dest_dir / img["filename"]
            self.download_image(
                filename=img["filename"],
                subfolder=img.get("subfolder", ""),
                img_type=img.get("type", "output"),
                dest_path=dest,
            )
            paths.append(dest)
        return paths


# ---------------------------------------------------------------------------
# Character database helpers
# ---------------------------------------------------------------------------

def load_personas(path: Path = PERSONAS_PATH) -> Dict:
    """Load the character personas database."""
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_character_slugs(personas: Dict) -> List[str]:
    """Return a sorted list of character slugs from the personas database."""
    characters = personas.get("characters", personas)
    if isinstance(characters, list):
        return sorted([c.get("slug", c.get("id", "")) for c in characters])
    if isinstance(characters, dict):
        return sorted(characters.keys())
    return []


def get_character(personas: Dict, slug: str) -> Dict:
    """Retrieve a single character's data by slug."""
    characters = personas.get("characters", personas)
    if isinstance(characters, list):
        for c in characters:
            if c.get("slug") == slug or c.get("id") == slug:
                return c
        raise KeyError(f"Character '{slug}' not found in personas database")
    if isinstance(characters, dict):
        if slug in characters:
            return characters[slug]
        raise KeyError(f"Character '{slug}' not found in personas database")
    raise ValueError("Unexpected personas format")


# ---------------------------------------------------------------------------
# ComfyUI settings loader
# ---------------------------------------------------------------------------

def load_comfyui_settings(path: Path = COMFYUI_SETTINGS_PATH) -> Dict:
    """Load comfyui_settings.json configuration."""
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Workflow builders
# ---------------------------------------------------------------------------

def build_master_workflow(
    character: Dict,
    prompt_text: str,
    negative_prompt: str,
    settings: Dict,
) -> Dict:
    """
    Build the ComfyUI API workflow JSON for Phase 1 (master image generation).

    This produces a Workflow-1 style prompt using the Z-Image-Turbo pipeline
    with sa_solver sampler, 30 steps, and RTX 5090 optimisations.
    """
    sampler_cfg = settings.get("default_sampler", {})
    slug = character.get("slug", character.get("id", "character"))

    workflow = {
        # -- Checkpoint Loader --
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": settings.get("default_checkpoint", "juggernautXL_v9.safetensors"),
            },
        },
        # -- CLIP Text Encode (positive) --
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt_text,
                "clip": ["1", 1],
            },
        },
        # -- CLIP Text Encode (negative) --
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": negative_prompt,
                "clip": ["1", 1],
            },
        },
        # -- Empty Latent Image --
        "4": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": sampler_cfg.get("width", 1024),
                "height": sampler_cfg.get("height", 1024),
                "batch_size": DEFAULT_BATCH_SIZE,
            },
        },
        # -- KSampler --
        "5": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["1", 0],
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["4", 0],
                "seed": int(time.time()) % (2**32),
                "steps": sampler_cfg.get("steps", 30),
                "cfg": sampler_cfg.get("cfg", 2.5),
                "sampler_name": sampler_cfg.get("sampler_name", "sa_solver"),
                "scheduler": sampler_cfg.get("scheduler", "karras"),
                "denoise": sampler_cfg.get("denoise", 1.0),
            },
        },
        # -- VAE Decode --
        "6": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["5", 0],
                "vae": ["1", 2],
            },
        },
        # -- Save Image --
        "7": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["6", 0],
                "filename_prefix": f"master_{slug}",
            },
        },
    }
    return workflow


def build_vault_workflow(
    character: Dict,
    prompt_text: str,
    negative_prompt: str,
    lora_path: str,
    settings: Dict,
) -> Dict:
    """
    Build the ComfyUI API workflow JSON for Phase 3 (vault generation).

    Uses Workflow-2 style prompt with the character's trained LoRA applied.
    """
    sampler_cfg = settings.get("default_sampler", {})
    slug = character.get("slug", character.get("id", "character"))

    workflow = {
        # -- Checkpoint Loader --
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": settings.get("default_checkpoint", "juggernautXL_v9.safetensors"),
            },
        },
        # -- LoRA Loader --
        "2": {
            "class_type": "LoraLoader",
            "inputs": {
                "model": ["1", 0],
                "clip": ["1", 1],
                "lora_name": lora_path,
                "strength_model": 0.85,
                "strength_clip": 0.85,
            },
        },
        # -- CLIP Text Encode (positive) --
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt_text,
                "clip": ["2", 1],
            },
        },
        # -- CLIP Text Encode (negative) --
        "4": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": negative_prompt,
                "clip": ["2", 1],
            },
        },
        # -- Empty Latent Image --
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": sampler_cfg.get("width", 1024),
                "height": sampler_cfg.get("height", 1024),
                "batch_size": DEFAULT_BATCH_SIZE,
            },
        },
        # -- KSampler --
        "6": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["2", 0],
                "positive": ["3", 0],
                "negative": ["4", 0],
                "latent_image": ["5", 0],
                "seed": int(time.time()) % (2**32),
                "steps": sampler_cfg.get("steps", 30),
                "cfg": sampler_cfg.get("cfg", 2.5),
                "sampler_name": sampler_cfg.get("sampler_name", "sa_solver"),
                "scheduler": sampler_cfg.get("scheduler", "karras"),
                "denoise": sampler_cfg.get("denoise", 1.0),
            },
        },
        # -- VAE Decode --
        "7": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["6", 0],
                "vae": ["1", 2],
            },
        },
        # -- Save Image --
        "8": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["7", 0],
                "filename_prefix": f"vault_{slug}",
            },
        },
    }
    return workflow


# ---------------------------------------------------------------------------
# Phase 1 -- Master Image Generation
# ---------------------------------------------------------------------------

def phase_generate_masters(
    client: ComfyUIClient,
    personas: Dict,
    settings: Dict,
    prompt_engine: PromptEngine,
    character_slug: Optional[str] = None,
    images_per_character: int = 3,
) -> ProgressTracker:
    """
    Generate master reference images for each character.

    Parameters
    ----------
    client : ComfyUIClient
        Connected ComfyUI API client.
    personas : dict
        Full personas database.
    settings : dict
        ComfyUI settings.
    prompt_engine : PromptEngine
        Initialised prompt engine for generating prompts.
    character_slug : str or None
        If provided, only generate for this character.
    images_per_character : int
        Number of master images per character (default 3).
    """
    slugs = [character_slug] if character_slug else get_character_slugs(personas)
    tracker = ProgressTracker(total=len(slugs) * images_per_character)

    logger.info(
        "=== PHASE 1: Master Image Generation === (%d characters, %d images each)",
        len(slugs),
        images_per_character,
    )

    for slug in slugs:
        character = get_character(personas, slug)
        char_dir = MASTER_IMAGES_DIR / slug
        char_dir.mkdir(parents=True, exist_ok=True)

        logger.info("Generating masters for character: %s", slug)

        for i in range(images_per_character):
            job = GenerationJob(
                prompt_id="",
                character_slug=slug,
                phase=PipelinePhase.MASTER_GEN,
            )
            tracker.jobs.append(job)

            # Build prompt using the prompt engine
            prompt_data = prompt_engine.generate_master_prompt(character, variation=i)
            prompt_text = prompt_data.get("positive", "")
            negative_prompt = prompt_data.get("negative", "")

            workflow = build_master_workflow(
                character, prompt_text, negative_prompt, settings
            )

            # Submit with retries
            for attempt in range(1, MAX_RETRIES + 1):
                job.attempts = attempt
                try:
                    prompt_id = client.queue_prompt(workflow)
                    job.prompt_id = prompt_id
                    job.status = "running"

                    status = client.wait_for_completion_ws(prompt_id, timeout=300)
                    job.status = status

                    if status == "completed":
                        files = client.download_prompt_outputs(prompt_id, char_dir)
                        job.output_files = [str(f) for f in files]
                        tracker.completed += 1
                        logger.info(
                            "  [%d/%d] Master %d for %s: OK (%d files)",
                            tracker.completed,
                            tracker.total,
                            i + 1,
                            slug,
                            len(files),
                        )
                        break
                    else:
                        raise RuntimeError(f"Generation failed with status: {status}")

                except Exception as exc:
                    logger.warning(
                        "  Attempt %d/%d failed for %s master %d: %s",
                        attempt,
                        MAX_RETRIES,
                        slug,
                        i + 1,
                        exc,
                    )
                    job.error = str(exc)
                    if attempt < MAX_RETRIES:
                        time.sleep(RETRY_DELAY_SECONDS * attempt)
                    else:
                        job.status = "failed"
                        tracker.failed += 1
                        logger.error(
                            "  FAILED: %s master %d after %d attempts",
                            slug,
                            i + 1,
                            MAX_RETRIES,
                        )

        logger.info(tracker.summary())

    return tracker


# ---------------------------------------------------------------------------
# Phase 2 -- LoRA Training Preparation
# ---------------------------------------------------------------------------

def phase_prepare_lora(
    personas: Dict,
    character_slug: Optional[str] = None,
) -> None:
    """
    Organise master images into kohya_ss training datasets.

    Delegates heavy lifting to ``prepare_lora_training.py`` which can be
    invoked as a subprocess or imported directly.
    """
    slugs = [character_slug] if character_slug else get_character_slugs(personas)

    logger.info("=== PHASE 2: LoRA Training Preparation === (%d characters)", len(slugs))

    prepare_script = SCRIPT_DIR / "prepare_lora_training.py"
    if not prepare_script.exists():
        raise FileNotFoundError(f"LoRA preparation script not found: {prepare_script}")

    for slug in slugs:
        logger.info("Preparing LoRA dataset for: %s", slug)
        cmd = [
            sys.executable,
            str(prepare_script),
            "--character",
            slug,
            "--master-dir",
            str(MASTER_IMAGES_DIR / slug),
            "--output-dir",
            str(LORA_DATASETS_DIR / slug),
            "--personas",
            str(PERSONAS_PATH),
            "--lora-config",
            str(LORA_CONFIG_PATH),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("LoRA prep failed for %s:\n%s", slug, result.stderr)
            raise RuntimeError(f"LoRA prep failed for {slug}")
        logger.info("  Dataset ready: %s", LORA_DATASETS_DIR / slug)

    logger.info("Phase 2 complete. Datasets in %s", LORA_DATASETS_DIR)
    logger.info(
        "Next step: run kohya_ss training for each character or use "
        "'generate-vault' after training is done."
    )


# ---------------------------------------------------------------------------
# Phase 3 -- Vault Content Generation
# ---------------------------------------------------------------------------

def phase_generate_vault(
    client: ComfyUIClient,
    personas: Dict,
    settings: Dict,
    prompt_engine: PromptEngine,
    character_slug: Optional[str] = None,
    images_per_character: int = 10,
) -> ProgressTracker:
    """
    Generate vault content images using trained LoRAs.

    Expects trained LoRA files at:
        output/lora_models/{slug}_lora_v1.safetensors
    """
    slugs = [character_slug] if character_slug else get_character_slugs(personas)
    tracker = ProgressTracker(total=len(slugs) * images_per_character)

    logger.info(
        "=== PHASE 3: Vault Content Generation === (%d characters, %d images each)",
        len(slugs),
        images_per_character,
    )

    for slug in slugs:
        character = get_character(personas, slug)
        lora_file = f"{slug}_lora_v1.safetensors"
        lora_path_full = LORA_MODELS_DIR / lora_file

        if not lora_path_full.exists():
            logger.error("LoRA not found for %s at %s -- skipping", slug, lora_path_full)
            tracker.failed += images_per_character
            continue

        char_vault_dir = VAULT_OUTPUT_DIR / slug
        char_vault_dir.mkdir(parents=True, exist_ok=True)

        logger.info("Generating vault content for: %s", slug)

        for i in range(images_per_character):
            job = GenerationJob(
                prompt_id="",
                character_slug=slug,
                phase=PipelinePhase.VAULT_GEN,
            )
            tracker.jobs.append(job)

            prompt_data = prompt_engine.generate_vault_prompt(character, variation=i)
            prompt_text = prompt_data.get("positive", "")
            negative_prompt = prompt_data.get("negative", "")

            workflow = build_vault_workflow(
                character, prompt_text, negative_prompt, lora_file, settings
            )

            for attempt in range(1, MAX_RETRIES + 1):
                job.attempts = attempt
                try:
                    prompt_id = client.queue_prompt(workflow)
                    job.prompt_id = prompt_id
                    job.status = "running"

                    status = client.wait_for_completion_ws(prompt_id, timeout=300)
                    job.status = status

                    if status == "completed":
                        files = client.download_prompt_outputs(prompt_id, char_vault_dir)
                        job.output_files = [str(f) for f in files]
                        tracker.completed += 1
                        logger.info(
                            "  [%d/%d] Vault image %d for %s: OK",
                            tracker.completed,
                            tracker.total,
                            i + 1,
                            slug,
                        )
                        break
                    else:
                        raise RuntimeError(f"Generation failed with status: {status}")

                except Exception as exc:
                    logger.warning(
                        "  Attempt %d/%d failed for %s vault %d: %s",
                        attempt,
                        MAX_RETRIES,
                        slug,
                        i + 1,
                        exc,
                    )
                    job.error = str(exc)
                    if attempt < MAX_RETRIES:
                        time.sleep(RETRY_DELAY_SECONDS * attempt)
                    else:
                        job.status = "failed"
                        tracker.failed += 1
                        logger.error(
                            "  FAILED: %s vault %d after %d attempts",
                            slug,
                            i + 1,
                            MAX_RETRIES,
                        )

        logger.info(tracker.summary())

    return tracker


# ---------------------------------------------------------------------------
# Full Pipeline
# ---------------------------------------------------------------------------

def run_full_pipeline(
    client: ComfyUIClient,
    personas: Dict,
    settings: Dict,
    prompt_engine: PromptEngine,
    character_slug: Optional[str] = None,
) -> None:
    """
    Execute the complete pipeline: masters -> LoRA prep -> vault generation.

    Note: LoRA training itself is performed externally (kohya_ss).  The
    pipeline will pause after Phase 2 and prompt the user to train before
    continuing to Phase 3.
    """
    logger.info("=" * 72)
    logger.info("FULL PIPELINE -- AI Influencer Image Generation")
    logger.info("RTX 5090 | 32GB VRAM | bf16 precision")
    logger.info("=" * 72)

    # Phase 1 ---------------------------------------------------------------
    master_tracker = phase_generate_masters(
        client, personas, settings, prompt_engine, character_slug
    )
    if master_tracker.failed > 0:
        logger.warning(
            "Phase 1 had %d failures. Review before continuing.", master_tracker.failed
        )

    # Phase 2 ---------------------------------------------------------------
    phase_prepare_lora(personas, character_slug)

    # Phase 3 -- requires trained LoRAs ------------------------------------
    logger.info("-" * 72)
    logger.info(
        "Phase 2 complete. Train LoRAs with kohya_ss before running Phase 3."
    )
    logger.info("LoRA datasets are in: %s", LORA_DATASETS_DIR)
    logger.info(
        "After training, place LoRA models in: %s", LORA_MODELS_DIR
    )
    logger.info(
        "Then run: python orchestrator.py generate-vault [--character SLUG]"
    )
    logger.info("-" * 72)

    # Check if LoRAs already exist and auto-continue
    slugs = [character_slug] if character_slug else get_character_slugs(personas)
    loras_ready = all(
        (LORA_MODELS_DIR / f"{s}_lora_v1.safetensors").exists() for s in slugs
    )
    if loras_ready:
        logger.info("All LoRAs found! Proceeding to Phase 3 automatically.")
        vault_tracker = phase_generate_vault(
            client, personas, settings, prompt_engine, character_slug
        )
        logger.info("Pipeline complete. %s", vault_tracker.summary())
    else:
        logger.info(
            "LoRAs not yet trained. Run 'generate-vault' after training."
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI Influencer Image Generation Pipeline Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  generate-masters   Phase 1: Generate master reference images
  prepare-lora       Phase 2: Prepare LoRA training datasets
  generate-vault     Phase 3: Generate vault content with trained LoRAs
  full-pipeline      Run all phases sequentially

Examples:
  %(prog)s generate-masters --character aria_nova
  %(prog)s prepare-lora
  %(prog)s generate-vault --character aria_nova
  %(prog)s full-pipeline
        """,
    )
    parser.add_argument(
        "command",
        choices=["generate-masters", "prepare-lora", "generate-vault", "full-pipeline"],
        help="Pipeline phase to execute",
    )
    parser.add_argument(
        "--character",
        type=str,
        default=None,
        help="Character slug to process (default: all 21 characters)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=DEFAULT_COMFYUI_HOST,
        help=f"ComfyUI host (default: {DEFAULT_COMFYUI_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_COMFYUI_PORT,
        help=f"ComfyUI port (default: {DEFAULT_COMFYUI_PORT})",
    )
    parser.add_argument(
        "--masters-count",
        type=int,
        default=3,
        help="Number of master images per character (default: 3)",
    )
    parser.add_argument(
        "--vault-count",
        type=int,
        default=10,
        help="Number of vault images per character (default: 10)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Ensure output directories exist
    for d in [MASTER_IMAGES_DIR, LORA_DATASETS_DIR, LORA_MODELS_DIR, VAULT_OUTPUT_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    # Load configuration
    logger.info("Loading personas from %s", PERSONAS_PATH)
    personas = load_personas()

    logger.info("Loading ComfyUI settings from %s", COMFYUI_SETTINGS_PATH)
    settings = load_comfyui_settings()

    # Initialise prompt engine
    prompt_engine = PromptEngine(personas=personas)

    # Initialise ComfyUI client (not needed for prepare-lora)
    client = None
    if args.command != "prepare-lora":
        client = ComfyUIClient(host=args.host, port=args.port)
        if not client.is_alive():
            logger.error(
                "Cannot reach ComfyUI at %s:%d. "
                "Ensure ComfyUI is running (see setup_environment.sh).",
                args.host,
                args.port,
            )
            sys.exit(1)
        gpu_info = client.check_gpu_memory()
        logger.info("GPU: %s (%.1f GB VRAM)", gpu_info.get("name", "?"), gpu_info.get("vram_total_gb", 0))

    # Dispatch
    if args.command == "generate-masters":
        tracker = phase_generate_masters(
            client,
            personas,
            settings,
            prompt_engine,
            character_slug=args.character,
            images_per_character=args.masters_count,
        )
        logger.info("Phase 1 done. %s", tracker.summary())

    elif args.command == "prepare-lora":
        phase_prepare_lora(personas, character_slug=args.character)

    elif args.command == "generate-vault":
        tracker = phase_generate_vault(
            client,
            personas,
            settings,
            prompt_engine,
            character_slug=args.character,
            images_per_character=args.vault_count,
        )
        logger.info("Phase 3 done. %s", tracker.summary())

    elif args.command == "full-pipeline":
        run_full_pipeline(
            client,
            personas,
            settings,
            prompt_engine,
            character_slug=args.character,
        )


if __name__ == "__main__":
    main()
