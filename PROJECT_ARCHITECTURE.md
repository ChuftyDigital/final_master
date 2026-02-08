# AI Influencer Image Pipeline - Project Architecture

## Overview

A fully automated, end-to-end image generation pipeline for 21 AI influencer characters, running on ComfyUI with RTX 5090 GPU. The system generates master reference images, trains per-character LoRAs, then produces a vault of 800 images per character across 4 content lanes.

## Pipeline Flow

```
CHARACTER DATA (personas.json)
        |
        v
+-------------------+
| PROMPT ENGINE     |  scripts/prompt_engine.py
| (Python)          |  Generates cinema-grade, character-specific prompts
+-------------------+
        |
        v
+-------------------+     +---------------------+
| WORKFLOW 1        | --> | 3 Master Images     |
| Master Image Gen  |     | per character (63)   |
| (ComfyUI)        |     +---------------------+
+-------------------+              |
                                   v
                    +----------------------------+
                    | LoRA TRAINING              |
                    | kohya_ss / sd-scripts      |
                    | 3 images -> character LoRA  |
                    +----------------------------+
                                   |
                                   v
+-------------------+     +---------------------+
| WORKFLOW 2        | --> | 800 Vault Images    |
| Vault Generator   |     | per character        |
| (ComfyUI)        |     | (16,800 total)       |
+-------------------+     +---------------------+
        |
        v
+-------------------+
| ORCHESTRATOR      |  scripts/orchestrator.py
| (Python)          |  Coordinates entire pipeline via ComfyUI API
+-------------------+
```

## Directory Structure

```
final_master/
|
|-- characters/
|   |-- personas.json              # Master character database (21 characters)
|
|-- config/
|   |-- comfyui_settings.json      # ComfyUI + Docker + GPU configuration
|   |-- content_lanes.json         # Content lane definitions (SFW/Suggestive/Spicy/NSFW)
|   |-- lora_training_config.json  # kohya_ss LoRA training parameters
|
|-- scripts/
|   |-- prompt_engine.py           # Core prompt generation engine
|   |-- orchestrator.py            # Master pipeline orchestrator
|   |-- prepare_lora_training.py   # LoRA dataset preparation
|   |-- setup_environment.sh       # Docker + environment setup
|
|-- workflows/
|   |-- workflow1_master_image_generator.json   # ComfyUI: Generate 3 master refs
|   |-- workflow2_vault_generator.json          # ComfyUI: Generate vault images
|   |-- PhotoFlow_Z-Image-Turbo_v2.0.json      # Reference: Original PhotoFlow
|   |-- ZIT Realism by HSWaggaNugget.json       # Reference: Original ZIT Realism
|
|-- output/
|   |-- master_images/             # Generated master reference images
|   |-- master_prompts/            # Generated prompt files for Workflow 1
|   |-- vault_manifests/           # Generated vault manifests + prompts
|   |-- lora_training/             # LoRA training datasets
|   |-- vault/                     # Final vault images (organized by character/lane)
|
|-- [Original reference docs]
    |-- AI_MODEL_PERSONAS_CHARACTER_GUIDE.txt
    |-- AI_MODEL_IMAGE_GENERATION_PROMPTS.txt
    |-- PREMIUM_PROMPT_GUIDE.md
    |-- PROMPT_AUTOMATION_GUIDE.md
    |-- MASTER_README.txt
    |-- prompts_premium_*.txt       # OLD prompts (superseded by prompt engine)
```

## Component Details

### 1. Character Database (`characters/personas.json`)

Single source of truth for all 21 characters. Contains:
- Physical attributes (height, build, hair, eyes, skin, face shape)
- Style information (clothing, accessories, makeup, aesthetic)
- Personality (traits, expression defaults, voice, vibe)
- Settings/locations appropriate to character niche
- Content pillars

**Key fix:** The old premium prompts used a broken template that gave nearly all characters identical physical descriptions. The new database has accurate, unique data per character.

### 2. Prompt Engine (`scripts/prompt_engine.py`)

The heart of the system. Generates prompts that are:
- **Character-specific:** Uses actual physical attributes, not templates
- **Cinema-grade:** 300-500+ words with professional photography terminology
- **Lane-aware:** Different clothing, mood, composition for each content tier
- **Bundle-structured:** Narrative arc for 3/5/10 image sets
- **Technically precise:** Camera specs, lighting setups, composition rules
- **Negative-prompt-aware:** Character-specific negative prompts

Commands:
```bash
python scripts/prompt_engine.py master          # Generate all 63 master prompts
python scripts/prompt_engine.py vault --char char_001  # Generate vault for one character
python scripts/prompt_engine.py vault-all       # Generate all 21 vault manifests
python scripts/prompt_engine.py test            # Quick test output
```

### 3. Workflow 1: Master Image Generator

ComfyUI workflow for generating 3 reference images per character.

Pipeline:
```
Z-Image-Turbo UNET + Qwen CLIP + UltraFlux VAE
  -> Style LoRA Stack (nicegirls + Photography + psxZStyle)
  -> 3x Parallel CLIPTextEncode (front/angle/natural prompts)
  -> 3x ClownsharKSampler (32 steps, exponential/krogstad, beta57)
  -> 3x VAEDecode
  -> 3x FaceDetailerPipe (1280px, dpmpp_2m, karras)
  -> 3x FastFilmGrain (0.015 amount)
  -> 3x SeedVR2VideoUpscaler (2048px target)
  -> 3x SaveImage
```

### 4. Workflow 2: Image Vault Generator

ComfyUI workflow for batch vault generation using trained LoRA + identity lock.

Pipeline:
```
Z-Image-Turbo + Character LoRA (0.85 strength)
  -> Style LoRA Stack (nicegirls + Photography + psxZStyle)
  -> IPAdapterFaceID (reference image identity lock, 0.75 strength)
  -> Scene Prompt + Identity Anchor combined conditioning
  -> BetaSamplingScheduler -> Sigma Rescale
  -> ClownsharKSampler (32 steps, exponential/krogstad)
  -> VAEDecode -> FaceDetailerPipe (SDXL auxiliary)
  -> FastFilmGrain -> ImageScaleBy (70%) -> SeedVR2 Upscale (2048px)
  -> SaveImage (organized naming)
```

Key feature: **Dual identity lock** via trained LoRA + IPAdapter FaceID ensures consistent face across all 800 images.

### 5. Content Lane System

| Lane | Images | Bundles | Description |
|------|--------|---------|-------------|
| SFW | 200 | 80 one-off + 10x3 + 10x5 + 4x10 | Fully clothed lifestyle |
| Suggestive | 200 | 80 one-off + 10x3 + 10x5 + 4x10 | Flirty, form-fitting |
| Spicy | 200 | 80 one-off + 10x3 + 10x5 + 4x10 | Lingerie, provocative |
| NSFW | 200 | 80 one-off + 10x3 + 10x5 + 4x10 | Artistic nudity, explicit |

**Per character total: 800 images**
**All 21 characters total: 16,800 images**

### 6. LoRA Training

Uses kohya_ss with settings optimized for:
- Very small dataset (3 images)
- RTX 5090 32GB VRAM
- Prodigy optimizer (adapts learning rate automatically)
- 1500 training steps
- network_dim=32, network_alpha=16
- bf16 mixed precision
- Regularization images for stability

### 7. RTX 5090 Optimizations

- **Docker:** `comfyui:latest-5090` (Blackwell architecture support)
- **Precision:** bf16 throughout (native 5090 support)
- **Attention:** SageAttention/FlashAttention enabled
- **VRAM:** 32GB allows larger batches and no model offloading
- **Compute:** ~2x faster than 4090 for diffusion inference

## Production Numbers

| Metric | Value |
|--------|-------|
| Characters | 21 |
| Master images | 63 (3 per character) |
| LoRA models | 21 (1 per character) |
| Vault images | 16,800 (800 per character) |
| Content lanes | 4 (SFW, Suggestive, Spicy, NSFW) |
| Bundle types | 3 (3-pack, 5-pack, 10-pack) |
| Est. time per character vault | 10-13 hours |
| Est. total pipeline time | ~12-15 days continuous |

## Quick Start

```bash
# 1. Set up environment
bash scripts/setup_environment.sh

# 2. Generate master prompts
python scripts/prompt_engine.py master

# 3. In ComfyUI: Load workflow1, generate master images

# 4. Prepare and run LoRA training
python scripts/prepare_lora_training.py --char char_001

# 5. Generate vault manifests
python scripts/prompt_engine.py vault-all

# 6. Run full pipeline (automated)
python scripts/orchestrator.py full-pipeline --char char_001

# Or run all characters:
python scripts/orchestrator.py full-pipeline --all
```
