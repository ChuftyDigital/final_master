# Super Factory Ultimate

Complete AI model character generation system. One unified CLI, clean architecture, real ComfyUI integration.

## What This Does

Generates thousands of photorealistic AI model images across 21 characters and 4 content lanes (SFW, Suggestive, Spicy, NSFW) using ComfyUI with Z-Image/FLUX models on GPU instances (RunPod, local RTX 4090/5090).

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Check system status
python main.py status

# 3. Install ComfyUI models (~30GB)
python main.py install --comfyui-path /workspace/ComfyUI

# 4. Generate reference images (3 per character)
python main.py references

# 5. Test with a small batch
python main.py generate --character 1 --lanes sfw --count 5

# 6. Full production run
python main.py generate
```

## Commands

| Command | Description |
|---------|-------------|
| `python main.py status` | Check setup: personas, refs, ComfyUI connection |
| `python main.py install --comfyui-path PATH` | Download all models and install custom nodes |
| `python main.py references` | Generate 3 reference face images per character |
| `python main.py generate` | Full batch generation across all lanes |
| `python main.py generate --lanes sfw --count 5` | Test run with small batch |
| `python main.py generate --dry-run` | Check readiness without generating |
| `python main.py prompts` | Export all prompts to text files |
| `python main.py workflow` | Export ComfyUI workflow JSON files |

## Project Structure

```
superfactory/             # Core Python package
  config.py               # Unified config management (config.yaml)
  cli.py                  # CLI with subcommands
  comfyui/
    client.py             # ComfyUI HTTP + WebSocket API client
    workflow_builder.py   # Programmatic workflow construction
  generation/
    prompt_engine.py      # Cinema-grade prompt generation
    reference_generator.py # Reference image generation (3 per char)
    batch_generator.py    # Bulk content with IPAdapter face consistency
  models/
    persona.py            # Persona data model with validation
    installer.py          # Model & custom node installer
  utils/
    logger.py             # Centralized logging

config.yaml               # All settings in one place
main.py                   # Single entry point
personas/                  # 21 character persona JSON files
templates/                 # Prompt templates per content lane
workflows/                 # Generated ComfyUI workflow exports
input/reference_images/    # Reference face images (3 per character)
output/                    # Generated content organized by character/lane
```

## Characters (21)

1. Isabella Reyes - Latina, Beach/Bikini Lifestyle
2. Arabella Pemberton-Clarke - English Equestrian
3. Giada Valentini - Italian Flight Attendant
4. Sasha Volkov - Russian Gamer
5. Zara Mitchell - Caribbean Fitness
6. Sakura Tanaka - Japanese Cosplay
7. Amelie Rousseau - French Fashion
8. Dakota Rose - Texas Girl Next Door
9. Valentina Sousa - Brazilian MILF
10. Priya Sharma - Indian Yoga
11. Luna Hart - Portland Alt/Tattoo
12. Mei Lin Chen - ASMR Girlfriend
13. Natasha Volkov - Berlin Dominatrix
14. Chloe Williams - Scottish College
15. Sienna Brooks - Australian Cougar
16. Jasmine Nguyen - Petite Asian
17. Ximena Morales - Mexican Curves
18. Scarlett Monroe - Southern BBW
19. Ebony Jackson - Black Beauty
20. Lena Kozlov - Lesbian Couples
21. Yuki Nakamura - Japanese Gamer

## Content Lanes

Each lane generates 200 images per character:
- **80** one-off images
- **10** bundles of 3 (30 images)
- **10** bundles of 5 (50 images)
- **4** bundles of 10 (40 images)

**Per character:** 800 images (4 lanes x 200)
**Total (21 chars):** 16,800 images

## Production Estimates

| Metric | Value |
|--------|-------|
| Per character | 3-6 hours, ~2GB |
| All 21 characters | 63-126 hours, ~42GB |
| RunPod cost (RTX 4090) | ~$30-50 |
| Per image time | ~15-20 seconds |

## Requirements

- Python 3.10+
- ComfyUI with Z-Image models
- NVIDIA GPU with 24GB+ VRAM (RTX 4090/5090 recommended)
- ~50GB disk space for models + output

## Key Improvements Over Original

- **Single CLI** instead of 25+ scattered scripts
- **Real ComfyUI API integration** with WebSocket progress (not placeholders)
- **Programmatic workflow builder** instead of fragile JSON files
- **Unified config.yaml** instead of hardcoded paths everywhere
- **Resume capability** with state tracking for interrupted batches
- **Cross-platform** paths (no more Windows-only or RunPod-only)
- **Clean Python package** with proper imports and structure
