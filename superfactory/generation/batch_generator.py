"""Batch content generator - mass-produces images across all lanes with face consistency."""

import json
import logging
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from superfactory.config import Config
from superfactory.comfyui.client import ComfyUIClient
from superfactory.comfyui.workflow_builder import build_bulk_workflow
from superfactory.generation.prompt_engine import PromptEngine
from superfactory.models.persona import Persona

logger = logging.getLogger("superfactory.batch")


class BatchGenerator:
    """Generates bulk content across all 4 lanes for one or more characters."""

    def __init__(self, config: Config, client: ComfyUIClient, prompt_engine: PromptEngine):
        self.config = config
        self.client = client
        self.prompts = prompt_engine
        self.output_base = config.path("output")
        self.ref_dir = config.path("reference_images")

        # Stats tracking
        self.stats = {
            "started": None,
            "characters_complete": 0,
            "characters_failed": 0,
            "images_generated": 0,
            "images_failed": 0,
        }

        # State file for resume capability
        self._state_file = config.base_dir / "logs" / "batch_state.json"
        self._state_file.parent.mkdir(parents=True, exist_ok=True)

    def _load_state(self) -> Dict[str, Any]:
        if self._state_file.exists():
            with open(self._state_file, "r") as f:
                return json.load(f)
        return {"completed": {}}

    def _save_state(self, state: Dict[str, Any]):
        with open(self._state_file, "w") as f:
            json.dump(state, f, indent=2)

    def _get_reference_images(self, persona: Persona) -> List[str]:
        """Get reference image paths for a character."""
        refs = []
        for name in persona.reference_image_names():
            path = self.ref_dir / name
            if path.exists():
                refs.append(str(path))
        return refs

    def generate_character(
        self,
        persona: Persona,
        lanes: Optional[List[str]] = None,
        count_override: Optional[int] = None,
    ) -> Dict[str, int]:
        """Generate all content for a single character across specified lanes.

        Returns dict of lane -> number of images generated.
        """
        if lanes is None:
            lanes = self.config.all_lanes()

        char_id = persona.character_id
        name = persona.name

        # Verify reference images
        ready, missing = persona.check_references(self.ref_dir)
        if not ready:
            logger.error(f"Missing reference images for {name}: {missing}")
            logger.error("Run 'superfactory references' first to generate them.")
            self.stats["characters_failed"] += 1
            return {}

        logger.info(f"Generating content for {name} ({char_id})")
        logger.info(f"  Lanes: {', '.join(lanes)}")

        results = {}
        state = self._load_state()

        for lane in lanes:
            lane_config = self.config.lane_config(lane)
            if not lane_config:
                logger.warning(f"  No config for lane '{lane}', skipping")
                continue

            # Calculate total images for this lane
            if count_override:
                total = count_override
            else:
                bundles = lane_config.get("bundles", {})
                total = (
                    bundles.get("one_off", 80)
                    + bundles.get("3x", 10) * 3
                    + bundles.get("5x", 10) * 5
                    + bundles.get("10x", 4) * 10
                )

            # Check resume state
            state_key = f"{char_id}:{lane}"
            already_done = state.get("completed", {}).get(state_key, 0)
            if already_done >= total:
                logger.info(f"  [{lane.upper()}] Already complete ({already_done}/{total})")
                results[lane] = already_done
                continue

            start_from = already_done
            logger.info(
                f"  [{lane.upper()}] Generating {total - start_from} images "
                f"(resuming from {start_from})" if start_from > 0 else
                f"  [{lane.upper()}] Generating {total} images"
            )

            # Create output directory
            lane_dir = self.output_base / f"{char_id}_{persona.safe_name}" / lane
            lane_dir.mkdir(parents=True, exist_ok=True)

            generated = start_from
            for idx in range(start_from, total):
                try:
                    prompt = self.prompts.bulk_prompt(persona, lane, idx)
                    negative = self.prompts.negative_prompt(lane)
                    seed = random.randint(1, 2**31)

                    workflow = build_bulk_workflow(
                        prompt=prompt,
                        checkpoint=self.config.model("bulk_checkpoint", "flux1-dev-fp8.safetensors"),
                        vae=self.config.model("vae", "ae.safetensors"),
                        text_encoder_t5=self.config.model("text_encoder_t5", "t5xxl_fp8_e4m3fn.safetensors"),
                        text_encoder_clip=self.config.model("text_encoder_clip", "clip_l.safetensors"),
                        clip_type=self.config.model("clip_type", "flux"),
                        width=self.config.generation("bulk", "resolution", [1024, 1536])[0],
                        height=self.config.generation("bulk", "resolution", [1024, 1536])[1],
                        steps=self.config.generation("bulk", "steps", 28),
                        cfg=self.config.generation("bulk", "cfg", 1.0),
                        sampler=self.config.generation("bulk", "sampler", "euler"),
                        scheduler=self.config.generation("bulk", "scheduler", "normal"),
                        seed=seed,
                        filename_prefix=f"{char_id}_{lane}_{idx:04d}",
                        negative=negative,
                        face_detail=self.config.generation("bulk", "face_detail", True),
                        face_detail_denoise=self.config.generation("bulk", "face_detail_denoise", 0.35),
                        upscale=self.config.generation("bulk", "upscale", False),
                    )

                    result = self.client.generate_and_wait(workflow)
                    files = self.client.save_images_from_output(
                        result["outputs"], lane_dir
                    )

                    if files:
                        generated += 1
                        self.stats["images_generated"] += 1
                    else:
                        self.stats["images_failed"] += 1

                    # Save progress periodically
                    if generated % 10 == 0:
                        state.setdefault("completed", {})[state_key] = generated
                        self._save_state(state)
                        logger.info(f"    Progress: {generated}/{total}")

                    # Brief pause between generations
                    time.sleep(0.3)

                except KeyboardInterrupt:
                    logger.info(f"Interrupted at image {generated}/{total}")
                    state.setdefault("completed", {})[state_key] = generated
                    self._save_state(state)
                    raise

                except Exception as e:
                    logger.error(f"    Image {idx} failed: {e}")
                    self.stats["images_failed"] += 1

            # Save final state
            state.setdefault("completed", {})[state_key] = generated
            self._save_state(state)
            results[lane] = generated
            logger.info(f"  [{lane.upper()}] Complete: {generated}/{total}")

        self.stats["characters_complete"] += 1
        return results

    def generate_all(
        self,
        personas: List[Persona],
        lanes: Optional[List[str]] = None,
        start_from: int = 0,
        count_override: Optional[int] = None,
    ):
        """Generate content for all characters."""
        self.stats["started"] = datetime.now()
        total = len(personas)

        logger.info("=" * 70)
        logger.info("MASTER BATCH GENERATION")
        logger.info(f"Characters: {total - start_from}")
        logger.info(f"Lanes: {lanes or self.config.all_lanes()}")
        logger.info("=" * 70)

        for i, persona in enumerate(personas[start_from:], start=start_from + 1):
            remaining = total - i
            self._print_progress(persona.name, remaining)
            self.generate_character(persona, lanes, count_override)
            time.sleep(1)

        self._print_final_report()

    def _print_progress(self, current: str, remaining: int):
        """Log current progress."""
        elapsed = ""
        if self.stats["started"]:
            delta = datetime.now() - self.stats["started"]
            h, r = divmod(int(delta.total_seconds()), 3600)
            m = r // 60
            elapsed = f"{h}h {m}m"

        logger.info(f"\n{'=' * 70}")
        logger.info(f"Current: {current} | Remaining: {remaining}")
        logger.info(
            f"Complete: {self.stats['characters_complete']} | "
            f"Images: {self.stats['images_generated']} | "
            f"Failed: {self.stats['images_failed']} | "
            f"Elapsed: {elapsed}"
        )
        logger.info("=" * 70)

    def _print_final_report(self):
        """Log final generation summary."""
        if self.stats["started"]:
            delta = datetime.now() - self.stats["started"]
            h, r = divmod(int(delta.total_seconds()), 3600)
            m = r // 60
            elapsed = f"{h}h {m}m"
        else:
            elapsed = "N/A"

        logger.info(f"\n{'=' * 70}")
        logger.info("BATCH GENERATION COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Total time: {elapsed}")
        logger.info(f"Characters complete: {self.stats['characters_complete']}")
        logger.info(f"Characters failed: {self.stats['characters_failed']}")
        logger.info(f"Images generated: {self.stats['images_generated']}")
        logger.info(f"Images failed: {self.stats['images_failed']}")
        logger.info(f"Output: {self.output_base}")
        logger.info("=" * 70)
