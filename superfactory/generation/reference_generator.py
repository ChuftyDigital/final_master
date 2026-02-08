"""Reference image generator - creates 3 consistent face references per character."""

import logging
from pathlib import Path
from typing import List, Optional

from superfactory.config import Config
from superfactory.comfyui.client import ComfyUIClient
from superfactory.comfyui.workflow_builder import build_reference_workflow
from superfactory.generation.prompt_engine import PromptEngine
from superfactory.models.persona import Persona

logger = logging.getLogger("superfactory.reference")


class ReferenceGenerator:
    """Generates 3 reference face images per character for identity consistency."""

    def __init__(self, config: Config, client: ComfyUIClient, prompt_engine: PromptEngine):
        self.config = config
        self.client = client
        self.prompts = prompt_engine
        self.output_dir = config.path("reference_images")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_character(
        self,
        persona: Persona,
        skip_existing: bool = True,
    ) -> List[Path]:
        """Generate all 3 reference images for a character.

        Returns list of saved image paths.
        """
        char_id = persona.character_id
        name = persona.name
        poses = self.config.generation("reference", "poses", ["front", "angle", "natural"])

        logger.info(f"Generating references for {name} ({char_id})")
        saved = []

        for i, pose in enumerate(poses, start=1):
            filename = f"{char_id}_face_{i:02d}.png"
            filepath = self.output_dir / filename

            # Skip if already exists
            if skip_existing and filepath.exists() and filepath.stat().st_size > 10000:
                logger.info(f"  [{i}/{len(poses)}] {filename} already exists, skipping")
                saved.append(filepath)
                continue

            logger.info(f"  [{i}/{len(poses)}] Generating {pose} pose...")

            # Generate prompt
            prompt = self.prompts.reference_prompt(persona, pose)
            negative = self.prompts.negative_prompt()

            # Build workflow (full photorealistic pipeline)
            workflow = build_reference_workflow(
                prompt=prompt,
                checkpoint=self.config.model("reference_checkpoint", "flux1-dev-fp8.safetensors"),
                vae=self.config.model("vae", "ae.safetensors"),
                text_encoder_t5=self.config.model("text_encoder_t5", "t5xxl_fp8_e4m3fn.safetensors"),
                text_encoder_clip=self.config.model("text_encoder_clip", "clip_l.safetensors"),
                clip_type=self.config.model("clip_type", "flux"),
                width=self.config.generation("reference", "resolution", [1024, 1024])[0],
                height=self.config.generation("reference", "resolution", [1024, 1024])[1],
                steps=self.config.generation("reference", "steps", 28),
                cfg=self.config.generation("reference", "cfg", 1.0),
                sampler=self.config.generation("reference", "sampler", "dpmpp_2m_sde_gpu"),
                scheduler=self.config.generation("reference", "scheduler", "karras"),
                filename_prefix=f"{char_id}_face_{i:02d}",
                negative=negative,
                face_detail=self.config.generation("reference", "face_detail", True),
                face_detail_denoise=self.config.generation("reference", "face_detail_denoise", 0.35),
                upscale=self.config.generation("reference", "upscale", True),
                upscale_model=self.config.generation("reference", "upscale_model", "4x-UltraSharp.pth"),
                upscale_megapixels=self.config.generation("reference", "upscale_megapixels", 4.0),
            )

            # Generate and save
            try:
                result = self.client.generate_and_wait(
                    workflow,
                    on_progress=lambda v, m, n: logger.debug(f"    Progress: {v}/{m}"),
                )
                files = self.client.save_images_from_output(
                    result["outputs"], self.output_dir, prefix=""
                )
                if files:
                    # Rename to standard naming if needed
                    src = files[0]
                    if src != filepath:
                        src.rename(filepath)
                    saved.append(filepath)
                    logger.info(f"  [{i}/{len(poses)}] Saved: {filename}")
                else:
                    logger.warning(f"  [{i}/{len(poses)}] No images returned")
            except Exception as e:
                logger.error(f"  [{i}/{len(poses)}] Failed: {e}")

        logger.info(f"  Result: {len(saved)}/{len(poses)} reference images")
        return saved

    def generate_all(
        self,
        personas: List[Persona],
        skip_existing: bool = True,
        start_from: int = 0,
    ) -> dict:
        """Generate references for all characters.

        Returns dict of character_id -> list of saved paths.
        """
        results = {}
        total = len(personas)

        for i, persona in enumerate(personas[start_from:], start=start_from + 1):
            logger.info(f"\n[{i}/{total}] Processing {persona.name}")
            paths = self.generate_character(persona, skip_existing)
            results[persona.character_id] = paths

        # Summary
        complete = sum(1 for v in results.values() if len(v) == 3)
        partial = sum(1 for v in results.values() if 0 < len(v) < 3)
        logger.info(f"\nReference generation complete: {complete} full, {partial} partial")
        return results
