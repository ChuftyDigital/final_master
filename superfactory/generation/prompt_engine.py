"""Unified prompt generation engine.

Generates cinema-grade natural language prompts optimized for Z-Image/FLUX models.
Handles reference prompts (3 poses) and bulk content prompts (4 lanes).
"""

import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

from superfactory.models.persona import Persona


class PromptEngine:
    """Generates all prompt types from persona data and templates."""

    def __init__(self, templates_dir: Optional[str] = None):
        self._templates: Dict[str, Any] = {}
        if templates_dir:
            self._load_templates(templates_dir)

    def _load_templates(self, directory: str):
        """Load lane-specific prompt templates."""
        d = Path(directory)
        for lane in ["sfw", "suggestive", "spicy", "nsfw"]:
            path = d / f"{lane}.json"
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    self._templates[lane] = json.load(f)

    # ── Physical Description Builder ──────────────────────────────────────

    def _build_physical_description(self, p: Persona) -> str:
        """Build a rich natural language physical description."""
        parts = []

        parts.append(
            f"She stands {p.height} tall with a {p.build} that exudes natural grace."
        )

        hair_flow = {
            "Long": "cascading past her shoulders with natural movement",
            "Medium": "flowing around her shoulders with soft texture",
            "Short": "styled elegantly, framing her face",
        }
        flow = hair_flow.get(p.hair_length, hair_flow["Medium"])
        parts.append(
            f"Her {p.hair_color.lower()} hair is {p.hair_texture.lower()} "
            f"and {p.hair_length.lower()}, {flow}."
        )

        eye_desc = {
            "Brown": "deep and expressive with warm undertones",
            "Blue": "vivid and striking with crystalline clarity",
            "Green": "vibrant and captivating with jewel-like intensity",
            "Hazel": "multifaceted with golden and green flecks",
            "Amber": "warm and luminous with honey-golden depths",
            "Gray": "cool and penetrating with silver undertones",
        }
        ed = eye_desc.get(p.eye_color, "striking and expressive")
        parts.append(
            f"Her {p.eye_color.lower()} {p.eye_shape.lower()}-shaped eyes are {ed}."
        )

        skin_desc = {
            "Warm olive": "a warm olive complexion that glows with natural radiance",
            "Porcelain": "porcelain skin with delicate, translucent quality",
            "Caramel": "a rich caramel skin tone radiating warmth",
            "Bronze": "a stunning bronze complexion that catches light beautifully",
        }
        sd = skin_desc.get(p.skin_tone, f"beautiful {p.skin_tone.lower()} skin with natural radiance")
        parts.append(f"She has {sd}.")

        if p.face_shape:
            parts.append(f"Her face has a {p.face_shape.lower()} shape.")

        if p.distinctive_features and p.distinctive_features.lower() != "unique natural beauty":
            parts.append(f"Distinctive features: {p.distinctive_features}.")

        return " ".join(parts)

    # ── Reference Image Prompts ───────────────────────────────────────────

    def reference_prompt(self, persona: Persona, pose: str) -> str:
        """Generate a cinema-grade reference image prompt.

        Args:
            persona: Character persona data.
            pose: One of 'front', 'angle', 'natural'.
        """
        p = persona
        physical = self._build_physical_description(p)
        personality = p.personality_summary.split(".")[0] if p.personality_summary else ""

        pose_specs = {
            "front": {
                "composition": (
                    f"Classic head-and-shoulders portrait with {p.name} positioned squarely "
                    f"facing the camera. Eyes at the upper third intersection. Frame captures "
                    f"mid-chest upward. Head straight with minimal tilt, conveying directness "
                    f"and confidence. Neutral expression with soft natural smile."
                ),
                "lighting": (
                    "Soft diffused studio lighting with large octagonal softbox at 45 degrees "
                    "above eye level. White reflector below chin for fill. Key light creates "
                    "gentle illumination emphasizing cheekbones. Color temperature 5600K. "
                    "Neutral background with subtle separation."
                ),
                "camera": (
                    "Sony A7R IV, 85mm f/1.4 GM lens at f/2.0. ISO 100, 1/200s. "
                    "Shallow depth of field, tack-sharp focus on both eyes."
                ),
            },
            "angle": {
                "composition": (
                    f"Elegant three-quarter view with {p.name}'s body at 45 degrees to camera, "
                    f"head turned back toward lens for dynamic eye contact. Reveals cheekbone "
                    f"and jawline structure. Shoulders relaxed. Gentle engaging smile reaching "
                    f"the eyes, creating warmth."
                ),
                "lighting": (
                    "Rembrandt-style lighting with key light at 45 degrees left, elevated 30 "
                    "degrees above eye level. Silver reflector for 2:1 fill ratio. Subtle hair "
                    "light from behind for separation and dimension."
                ),
                "camera": (
                    "Canon EOS R5, 50mm f/1.2 L at f/1.8. ISO 200, 1/160s. "
                    "Dual pixel AF on near eye. Creamy bokeh with sharp subject."
                ),
            },
            "natural": {
                "composition": (
                    f"Candid-inspired environmental portrait of {p.name} in a relaxed, "
                    f"spontaneous moment. Asymmetrical organic pose with slight lean. "
                    f"Head gently tilted. Warm genuine smile with eyes crinkled at corners. "
                    f"Documentary quality that feels like a real captured moment."
                ),
                "lighting": (
                    "Natural window light from large north-facing window. Soft diffused "
                    "illumination with gentle highlight-to-shadow transitions. V-board "
                    "reflector opposite window for fill. 5500K natural daylight."
                ),
                "camera": (
                    "Sony A7R IV, 35mm f/1.4 GM at f/1.8. ISO 400, 1/250s. "
                    "Wider perspective for environmental storytelling with subject separation."
                ),
            },
        }

        spec = pose_specs.get(pose, pose_specs["front"])

        prompt = (
            f"Professional portrait photograph of {p.name}, a {p.age}-year-old "
            f"{p.ethnicity} woman of {p.nationality} heritage. "
            f"{physical} "
            f"Styled in {p.fashion_sense} reflecting {p.aesthetic.lower()} aesthetic. "
            f"{personality}. "
            f"Composition: {spec['composition']} "
            f"Lighting: {spec['lighting']} "
            f"Camera: {spec['camera']} "
            f"Photorealistic 8K, natural skin texture with visible pores, "
            f"individual hair strands, realistic catchlights in eyes. "
            f"Magazine-quality portrait, not AI-generated looking."
        )

        return " ".join(prompt.split())

    # ── Bulk Content Prompts ──────────────────────────────────────────────

    def bulk_prompt(self, persona: Persona, lane: str, index: int = 0) -> str:
        """Generate a content prompt for bulk image generation.

        Uses templates if available, otherwise generates dynamically.
        """
        p = persona
        templates = self._templates.get(lane, {})

        # Build base character description
        base = (
            f"Photorealistic photograph of {p.name}, {p.age}-year-old {p.ethnicity} woman. "
            f"{p.hair_color} {p.hair_length.lower()} {p.hair_texture.lower()} hair, "
            f"{p.eye_color.lower()} {p.eye_shape.lower()} eyes, "
            f"{p.skin_tone.lower()} skin, {p.build}."
        )

        # Get scenario from templates or generate dynamically
        scenario = self._get_scenario(p, lane, templates, index)

        # Build quality modifiers based on lane
        quality = self._lane_quality(lane)

        # Pick random location and wardrobe
        location = random.choice(p.locations) if p.locations else "indoor setting"
        outfit = random.choice(p.wardrobe) if p.wardrobe else "stylish outfit"

        prompt = (
            f"{base} {scenario} "
            f"Location: {location}. Wearing {outfit}. "
            f"{quality}"
        )

        return " ".join(prompt.split())

    def _get_scenario(
        self, p: Persona, lane: str, templates: Dict, index: int
    ) -> str:
        """Get a scenario description for the given lane."""
        micro_templates = templates.get("micro_influencer_templates", [])
        if micro_templates:
            template = micro_templates[index % len(micro_templates)]
            # Simple variable substitution
            return template.replace("{name}", p.name).replace("{age}", str(p.age))

        # Default scenarios by lane
        scenarios = {
            "sfw": [
                "Professional fashion shoot, confident pose, editorial quality.",
                "Lifestyle moment in upscale setting, natural and approachable.",
                "Fitness portrait showing strength and grace, clean background.",
                "Travel content in picturesque location, warm golden light.",
                "Coffee shop aesthetic, relaxed pose, morning light.",
            ],
            "suggestive": [
                "Glamour portrait, alluring gaze, tasteful and sophisticated.",
                "Beach sunset portrait, wind in hair, flirty expression.",
                "Boudoir-style in elegant setting, soft warm lighting.",
                "Evening wear photoshoot, mysterious and captivating mood.",
                "Poolside glamour, confident and sensual, golden hour.",
            ],
            "spicy": [
                "Intimate portrait, provocative pose, dramatic lighting.",
                "Lingerie editorial, steamy atmosphere, studio quality.",
                "Bedroom setting, bold and confident, artistic composition.",
                "Bathtub scene, artistic and tasteful, moody lighting.",
                "Close-up intimate portrait, intense gaze, shallow DOF.",
            ],
            "nsfw": [
                "Artistic adult portrait, confident expression, professional quality.",
                "Intimate scene, natural lighting, authentic and unposed.",
                "Bold artistic nude, dramatic shadows, editorial quality.",
                "Private moment captured, genuine expression, warm tones.",
                "Sensual portrait, artistic composition, premium quality.",
            ],
        }

        lane_scenarios = scenarios.get(lane, scenarios["sfw"])
        return lane_scenarios[index % len(lane_scenarios)]

    def _lane_quality(self, lane: str) -> str:
        """Get quality modifiers appropriate for the lane."""
        base = (
            "Photorealistic, natural skin texture, sharp focus, "
            "professional photography, film grain."
        )
        extras = {
            "sfw": "Shot on Sony A7R IV, 85mm f/1.8, clean bright lighting.",
            "suggestive": "Cinematic color grading, warm tones, soft bokeh.",
            "spicy": "Dramatic lighting, rich shadows, intimate atmosphere.",
            "nsfw": "Artistic quality, natural lighting, authentic mood.",
        }
        return f"{base} {extras.get(lane, extras['sfw'])}"

    def negative_prompt(self, lane: str = "sfw") -> str:
        """Get an appropriate negative prompt (for non-Z-Image models)."""
        return (
            "blurry, low quality, distorted face, bad anatomy, deformed, "
            "plastic skin, watermark, text, cartoon, anime, 3d render, "
            "extra limbs, missing limbs, bad eyes, crossed eyes"
        )
