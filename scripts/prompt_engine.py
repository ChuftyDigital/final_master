#!/usr/bin/env python3
"""
AI Influencer Prompt Engine v2.0
================================
Cinema-grade prompt generation system that produces character-specific,
highly detailed prompts for Z-Image-Turbo / ComfyUI generation.

This engine reads the character persona database and generates prompts
that are faithful to each character's unique physical attributes,
personality, niche, and aesthetic.

Used by both Workflow 1 (Master Images) and Workflow 2 (Vault Generation).
"""

import json
import os
import random
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CHARACTERS_FILE = BASE_DIR / "characters" / "personas.json"
LANES_FILE = BASE_DIR / "config" / "content_lanes.json"

# ---------------------------------------------------------------------------
# Camera & Technical Presets
# ---------------------------------------------------------------------------
CAMERA_PRESETS = {
    "portrait_studio": {
        "camera": "Sony A7R V full-frame mirrorless camera",
        "lens": "Sony FE 85mm f/1.4 GM",
        "aperture": "f/1.8",
        "iso": "100",
        "shutter": "1/200s",
        "white_balance": "5600K daylight balance",
        "resolution": "photorealistic 8K resolution"
    },
    "environmental": {
        "camera": "Canon EOS R5 Mark II full-frame mirrorless",
        "lens": "Canon RF 50mm f/1.2L USM",
        "aperture": "f/2.8",
        "iso": "200",
        "shutter": "1/250s",
        "white_balance": "auto white balance with natural tones",
        "resolution": "photorealistic 8K resolution"
    },
    "intimate": {
        "camera": "Nikon Z9 full-frame mirrorless",
        "lens": "Nikkor Z 85mm f/1.2 S",
        "aperture": "f/1.4",
        "iso": "400",
        "shutter": "1/125s",
        "white_balance": "3800K warm tungsten balance",
        "resolution": "photorealistic 8K resolution"
    },
    "action": {
        "camera": "Sony A1 full-frame mirrorless",
        "lens": "Sony FE 70-200mm f/2.8 GM OSS II",
        "aperture": "f/2.8",
        "iso": "800",
        "shutter": "1/500s",
        "white_balance": "5200K mixed light balance",
        "resolution": "photorealistic 8K resolution"
    },
    "fashion": {
        "camera": "Hasselblad X2D 100C medium format",
        "lens": "Hasselblad XCD 80mm f/1.9",
        "aperture": "f/2.0",
        "iso": "64",
        "shutter": "1/160s",
        "white_balance": "5500K controlled studio balance",
        "resolution": "photorealistic ultra-high resolution, medium format detail"
    }
}

LIGHTING_SETUPS = {
    "soft_studio": (
        "Soft diffused studio lighting with a large octagonal softbox positioned "
        "45 degrees from camera axis and slightly above eye level. A white reflector "
        "below chin provides subtle fill, eliminating harsh shadows while maintaining "
        "natural dimensionality. Color temperature calibrated to 5600K daylight balance."
    ),
    "rembrandt": (
        "Rembrandt-style lighting with key light at 45 degrees to the subject's left, "
        "elevated 30 degrees above eye level, creating the characteristic triangular "
        "highlight on the shadow-side cheek. Silver reflector provides controlled fill "
        "at 2:1 ratio. Subtle hair light from behind adds separation and dimension."
    ),
    "natural_window": (
        "Large window providing soft, directional natural light from camera-left. "
        "Sheer curtains diffuse the sunlight creating gentle, wrapping illumination. "
        "A subtle warm fill from the room's ambient light prevents deep shadows. "
        "The quality mimics a painter's north-facing studio light."
    ),
    "golden_hour": (
        "Natural golden hour sunlight streaming in at a low angle, creating warm "
        "amber tones and long soft shadows. The backlit quality creates a natural "
        "rim light effect around hair and shoulders. Fill from reflected warm surfaces "
        "prevents loss of facial detail in shadows."
    ),
    "moody_intimate": (
        "Low-key lighting with a single warm light source positioned to one side, "
        "creating dramatic shadows and intimacy. Candles or practicals in frame add "
        "depth and atmosphere. The warm 3200K color temperature creates a sensual, "
        "intimate mood with rich skin tones."
    ),
    "dramatic_shadows": (
        "High-contrast dramatic lighting with hard key light from above-left, "
        "creating defined shadows that sculpt the face and body. Minimal fill "
        "allows deep shadows for a noir-inspired mood. Rim light creates striking "
        "edge definition against the dark background."
    ),
    "bright_airy": (
        "Bright, even studio lighting with multiple diffused sources creating "
        "a clean, airy feel. Two large softboxes at 45 degrees with a beauty "
        "dish overhead. Fill reflectors minimize shadows for a fresh, commercial "
        "photography aesthetic. 5800K slightly cool balance."
    ),
    "neon_ambient": (
        "Colorful ambient LED lighting creating vibrant color washes. RGB strip "
        "lights provide colored fills from multiple angles. The mixed color "
        "temperature creates a modern, energetic atmosphere typical of gaming "
        "setups and nightlife scenes."
    )
}

# ---------------------------------------------------------------------------
# Scene/Scenario Generators per Niche
# ---------------------------------------------------------------------------
NICHE_SCENARIOS = {
    "Beach/Bikini Lifestyle": {
        "sfw": [
            "walking along the shoreline at golden hour, barefoot in sundress",
            "sitting on a beach towel reading a book, ocean waves in background",
            "leaning against a lifeguard tower, casual beachwear, windswept hair",
            "at an outdoor cafe by the marina, sipping a smoothie",
            "on a pier at sunset, casual outfit, hair blowing in sea breeze",
            "exploring tide pools, crouched down, curious expression",
            "at a beach volleyball game, cheering from sideline",
            "morning jog on the beach, athletic wear, sunrise background"
        ],
        "suggestive": [
            "emerging from the ocean, bikini, water droplets on skin, sunlit",
            "lying on a beach lounger, sunbathing, looking over sunglasses",
            "at a pool party, wet hair, playful splashing moment",
            "applying sunscreen to shoulders, bikini top, flirty look back",
            "stretching on the beach in fitted activewear at sunrise",
            "leaning against a yacht railing, wind catching a flowing sarong",
            "outdoor shower by the beach, washing sand off, eyes closed",
            "sitting on rocks by the ocean, legs drawn up, wet bikini"
        ],
        "spicy": [
            "in a luxury beach cabana, sheer cover-up barely concealing bikini",
            "reclining on a daybed by the pool, string bikini, inviting gaze",
            "bedroom with ocean view, wearing lingerie, morning light",
            "in an outdoor shower, water cascading, minimal swimwear",
            "on silk sheets, beach house bedroom, wearing delicate lingerie set",
            "private hot tub on deck, steam rising, shoulders visible above water",
            "untying bikini top while lying face-down on beach towel",
            "standing in doorframe of beach house, backlit, silky robe falling open"
        ],
        "nsfw": [
            "artistic nude on private beach at golden hour, tasteful body positioning",
            "in a luxury bathtub overlooking the ocean, candlelit, partial immersion",
            "on white sheets with tropical flowers, nude figure study, soft light",
            "private outdoor shower, full figure, water streaming, natural beauty",
            "reclining on chaise by private pool, nude sunbathing, serene expression",
            "bedroom with billowing curtains, nude on bed, editorial pose",
            "standing at floor-to-ceiling window, silhouette view, artistic framing",
            "floating in an infinity pool, minimalist artistic nude"
        ]
    },
    "Equestrian/Country Elite": {
        "sfw": [
            "standing with horse in stable, wearing riding attire, commanding pose",
            "in a country manor library, reading by fireplace, elegant casual",
            "walking through manicured gardens, tailored outfit, aristocratic bearing",
            "at polo grounds, watching match, champagne in hand",
            "in the study, seated at antique desk, power pose",
            "grooming a horse, riding jacket removed, rolled sleeves",
            "on country estate grounds, walking dogs, Wellington boots",
            "at a country pub, seated elegantly, knowing smile"
        ],
        "suggestive": [
            "in riding breeches and fitted blouse, top buttons undone, stable backdrop",
            "seated on leather sofa by fire, silk blouse, legs crossed elegantly",
            "after riding, slightly disheveled, hair coming undone, flushed cheeks",
            "in a silk robe at the manor window, morning light, coffee in hand",
            "wearing a figure-hugging cocktail dress for country ball, staircase pose",
            "in jodhpurs and corset-style top, riding crop in hand, commanding look",
            "lounging in drawing room, silk pajamas, reading with wine",
            "standing at stable door, shirt dampened, confident posture"
        ],
        "spicy": [
            "in the bedroom of the manor, silk lingerie, four-poster bed",
            "wearing riding corset and stockings, sitting on bed edge",
            "in a deep copper bathtub, manor bathroom, candlelit",
            "silk robe open, standing before ornate mirror, morning light",
            "on a chaise longue, lace lingerie, fireplace glow",
            "in riding boots and lingerie only, stable-inspired boudoir",
            "bedroom scene, silk sheets, pearl necklace only",
            "at vanity table, applying lipstick, wearing sheer negligee"
        ],
        "nsfw": [
            "artistic nude on four-poster bed, silk sheets, manor bedroom",
            "standing before floor-length mirror, nude study, golden firelight",
            "in copper bathtub, figure emerging from water, candlelit beauty",
            "on fur throw before fireplace, artistic nude, warm shadows",
            "classical figure study in manor gallery, natural light from tall windows",
            "on silk chaise, nude odalisque pose, renaissance painting quality",
            "private chamber, standing at window, backlit nude silhouette",
            "in garden folly, natural nude, classical sculpture reference"
        ]
    },
    "default": {
        "sfw": [
            "casual lifestyle portrait in character-appropriate setting",
            "sitting comfortably in natural pose, genuine expression",
            "standing in signature location, confident but relaxed",
            "candid moment during everyday activity",
            "environmental portrait showing personality through surroundings",
            "walking scene, natural movement, lifestyle feel",
            "sitting at favorite spot, engaged with hobby or interest",
            "morning routine moment, natural and authentic"
        ],
        "suggestive": [
            "wearing form-fitting outfit, confident pose, playful energy",
            "getting ready, mirror reflection, applying finishing touches",
            "lounging in fitted clothing, relaxed but aware of camera",
            "looking over shoulder, fitted outfit showing figure",
            "reclining casually, clothing riding up slightly, natural pose",
            "stretching or reaching, body language suggesting confidence",
            "wet hair fresh from shower, wrapped in towel at vanity",
            "fitted dress or outfit, seated with legs crossed, teasing smile"
        ],
        "spicy": [
            "wearing lingerie in bedroom, intimate lighting, inviting pose",
            "on bed in intimate wear, sheets partially covering",
            "in bathroom mirror, wearing bra and underwear, getting undressed",
            "silk robe falling off shoulder, bedroom setting, warm light",
            "lying on stomach in lingerie, looking back at camera",
            "standing in doorway, backlit, sheer fabric revealing silhouette",
            "on luxurious bedding, lace lingerie, intimate gaze",
            "at vanity, partially dressed, candlelit atmosphere"
        ],
        "nsfw": [
            "artistic nude on bed, tasteful positioning, soft lighting",
            "in bathtub, water partially covering, intimate atmosphere",
            "standing figure study, natural light, editorial quality",
            "reclining nude on sheets, artistic composition",
            "shower scene, water streaming, natural beauty",
            "bed scene from above, artistic nude, creative framing",
            "silhouette at window, full figure, dramatic backlight",
            "private moment, nude study, warm intimate lighting"
        ]
    }
}

# Add more niche-specific scenarios
for niche in [
    "Luxury Travel/Aviation", "Gaming/E-Sports (Cute/Casual)",
    "Fitness/Athletic Training", "Cosplay/Anime", "Fashion/Haute Couture",
    "Amateur/Girl Next Door", "MILF/Mature Latina", "Yoga/Wellness/Spiritual",
    "Alternative/Tattooed", "ASMR/Girlfriend Experience", "Dominatrix/BDSM",
    "College/Young Adult (18+)", "MILF/Cougar", "Petite Asian/Feet Content",
    "Latina Curves/BBW", "BBW/Southern Charm", "Black Beauty/Melanin Content",
    "Lesbian/Couples Content", "Sexy Japanese Gamer/Competitive Streaming"
]:
    if niche not in NICHE_SCENARIOS:
        NICHE_SCENARIOS[niche] = NICHE_SCENARIOS["default"]


# ---------------------------------------------------------------------------
# Core Data Loader
# ---------------------------------------------------------------------------
def load_characters():
    """Load the character database."""
    with open(CHARACTERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {c["id"]: c for c in data["characters"]}


def load_lanes():
    """Load the content lane definitions."""
    with open(LANES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Prompt Builders
# ---------------------------------------------------------------------------
def build_physical_description(char: dict) -> str:
    """Build a rich, character-specific physical description block."""
    p = char["physical"]
    parts = [
        f"She stands {p['height']} tall with a {p['build']}.",
        f"Her hair is {p['hair_color']}, {p['hair_length']} in length, "
        f"{p['hair_texture']}.",
        f"Her eyes are {p['eye_color']}, {p['eye_shape']}.",
        f"She has {p['skin_tone']} skin that is {p['skin_texture']}.",
        f"Her face features {p['face_shape']}.",
    ]
    if p.get("distinguishing_features"):
        parts.append(f"Notable features: {p['distinguishing_features']}.")
    return " ".join(parts)


def build_clothing_description(char: dict, lane: str) -> str:
    """Build lane-appropriate clothing description from character wardrobe."""
    style = char["style"]
    clothing_pool = style["typical_clothing"]
    accessories_pool = style["accessories"]

    if lane == "sfw":
        items = [c for c in clothing_pool if not any(
            word in c.lower() for word in ["lingerie", "bikini", "underwear", "bra"]
        )]
        if not items:
            items = clothing_pool[:3]
        chosen = random.choice(items) if items else "casual clothing"
        acc = random.choice(accessories_pool) if accessories_pool else ""
        return f"wearing {chosen}" + (f", {acc}" if acc else "")

    elif lane == "suggestive":
        items = [c for c in clothing_pool if any(
            word in c.lower() for word in [
                "fitted", "form", "tight", "crop", "bikini", "dress", "legging"
            ]
        )]
        if not items:
            items = clothing_pool
        chosen = random.choice(items)
        return f"wearing a flattering {chosen}, showing off her figure"

    elif lane == "spicy":
        return f"wearing delicate lingerie that complements her {char['physical']['skin_tone']} skin"

    elif lane == "nsfw":
        return "minimal clothing or artistic nudity, tasteful positioning"

    return f"wearing {random.choice(clothing_pool)}"


def build_scene_description(char: dict, lane: str, scenario_override: str = None) -> str:
    """Build a scene/setting appropriate to the character and lane."""
    if scenario_override:
        return scenario_override

    niche = char["niche"]
    scenarios = NICHE_SCENARIOS.get(niche, NICHE_SCENARIOS["default"])
    lane_scenarios = scenarios.get(lane, scenarios.get("sfw", []))
    if lane_scenarios:
        return random.choice(lane_scenarios)
    return f"in a character-appropriate setting, {random.choice(char['settings'])}"


def build_technical_block(preset_key: str = "portrait_studio") -> str:
    """Build the technical camera/settings block."""
    preset = CAMERA_PRESETS[preset_key]
    return (
        f"Technical Specifications: Captured with {preset['camera']} paired with "
        f"{preset['lens']}. Aperture set to {preset['aperture']} for shallow depth "
        f"of field isolating the subject. ISO {preset['iso']}, shutter speed "
        f"{preset['shutter']}. White balance {preset['white_balance']}. "
        f"Rendered in {preset['resolution']} with exceptional detail - individual "
        f"hair strands, natural skin texture with visible pores and subtle "
        f"imperfections, fine fabric detail. Color grading maintains natural skin "
        f"tones with professional contrast. Post-processing retains natural texture "
        f"while optimizing contrast and color accuracy."
    )


def build_quality_requirements() -> str:
    """Build the critical quality requirements block."""
    return (
        "Critical Requirements: Photorealistic quality with natural skin texture - "
        "every pore, fine line, and natural imperfection visible. Hair appears as "
        "individual strands with natural variation. Eyes have realistic catchlights "
        "and depth. The image looks captured by a master portrait photographer, not "
        "AI-generated. No artificial smoothness, no plastic appearance, no exaggerated "
        "features - only authentic natural beauty with technical excellence."
    )


# ---------------------------------------------------------------------------
# Master Image Prompts (Workflow 1)
# ---------------------------------------------------------------------------
def generate_master_prompt(char: dict, pose_type: str = "front") -> str:
    """
    Generate a cinema-grade prompt for master reference image generation.

    pose_type: 'front', 'angle', 'natural'
    """
    name = char["name"]
    physical_desc = build_physical_description(char)

    if pose_type == "front":
        composition = (
            f"Classic head-and-shoulders portrait with {name} positioned squarely "
            f"facing the camera, shoulders aligned with frame. Rule of thirds "
            f"composition with eyes along upper third line. Frame captures from "
            f"mid-chest upward. Head straight with minimal tilt, conveying directness "
            f"and confidence. Expression is {char['personality']['expression_default']}. "
            f"This frontal approach creates the most accurate representation for "
            f"facial recognition and identity consistency."
        )
        lighting = LIGHTING_SETUPS["soft_studio"]
        camera = "portrait_studio"

    elif pose_type == "angle":
        composition = (
            f"Elegant three-quarter view with {name}'s body at 45-degree angle to "
            f"camera while head turns toward lens, creating dynamic yet natural pose. "
            f"This positioning reveals full facial structure while maintaining eye "
            f"contact. Emphasizes cheekbones and jawline through angular perspective. "
            f"Shoulders relaxed with subtle turn creating elegant lines. Expression "
            f"features {char['personality']['expression_default']}. Provides crucial "
            f"three-dimensional facial reference."
        )
        lighting = LIGHTING_SETUPS["rembrandt"]
        camera = "portrait_studio"

    elif pose_type == "natural":
        setting = random.choice(char["settings"][:3])
        composition = (
            f"Environmental portrait of {name} in {setting}. Natural, candid-feeling "
            f"pose that shows personality and character context. The composition "
            f"includes environmental elements that reflect her {char['niche']} niche. "
            f"Three-quarter to full body framing with shallow depth of field keeping "
            f"subject sharp against softly blurred setting. Expression captures "
            f"{char['personality']['expression_default']} in a natural, unguarded moment."
        )
        lighting = LIGHTING_SETUPS["natural_window"]
        camera = "environmental"

    else:
        raise ValueError(f"Unknown pose_type: {pose_type}")

    # Build the character-specific clothing for master images (always SFW/presentable)
    clothing = build_clothing_description(char, "sfw")

    prompt = (
        f"Subject: Professional portrait photograph of {name}, a {char['age']}-year-old "
        f"{char['ethnicity']} woman with {char['heritage']} heritage. "
        f"Physical Description: {physical_desc} "
        f"She is {clothing}. "
        f"Composition & Pose: {composition} "
        f"Lighting: {lighting} "
        f"{build_technical_block(camera)} "
        f"Style & Atmosphere: The image embodies {char['personality']['vibe']} with "
        f"a timeless, editorial quality. The overall mood is sophisticated and "
        f"authentic to the character. "
        f"{build_quality_requirements()}"
    )
    return prompt


def generate_master_negative_prompt(char: dict) -> str:
    """Generate character-aware negative prompt for master images."""
    base = (
        "cartoon, anime style, illustration, painting, drawing, CGI, 3D render, "
        "low quality, blurry, distorted features, multiple people, deformed, "
        "mutation, extra limbs, text, watermark, signature, frame, border, "
        "bad anatomy, unrealistic proportions, different person, inconsistent features, "
        "plastic skin, artificial smoothness, overprocessed, HDR artifacts, "
        "oversaturated, deep fried, JPEG artifacts"
    )

    # Add character-specific negatives
    p = char["physical"]
    negatives = []

    # Negate wrong hair
    if "blonde" not in p["hair_color"].lower():
        negatives.append("blonde hair")
    if "black" not in p["hair_color"].lower() and "dark" not in p["hair_color"].lower():
        negatives.append("black hair")
    if "red" not in p["hair_color"].lower() and "auburn" not in p["hair_color"].lower():
        negatives.append("red hair")

    # Negate wrong build
    if "petite" in p["build"].lower() or "slim" in p["build"].lower():
        negatives.append("overweight, chubby")
    elif "full" in p["build"].lower() or "voluptuous" in p["build"].lower() or "curvy" in p["build"].lower():
        negatives.append("thin, skinny, underweight")

    # Negate wrong skin tone
    if "dark" in p["skin_tone"].lower() or "melanin" in p["skin_tone"].lower():
        negatives.append("pale skin, light skin, white skin")
    elif "pale" in p["skin_tone"].lower() or "fair" in p["skin_tone"].lower() or "porcelain" in p["skin_tone"].lower():
        negatives.append("dark skin, tanned")

    if negatives:
        return base + ", " + ", ".join(negatives)
    return base


# ---------------------------------------------------------------------------
# Vault Image Prompts (Workflow 2)
# ---------------------------------------------------------------------------
def generate_vault_prompt(
    char: dict,
    lane: str,
    scenario: str = None,
    bundle_context: str = None,
    image_index_in_bundle: int = 0,
    bundle_size: int = 1
) -> str:
    """
    Generate a prompt for vault image generation.

    char: Character data dict
    lane: 'sfw', 'suggestive', 'spicy', 'nsfw'
    scenario: Optional scenario override
    bundle_context: Optional theme for bundle (e.g., "beach day photoshoot")
    image_index_in_bundle: Position in bundle (0-indexed)
    bundle_size: Total images in bundle (1 for one-offs)
    """
    name = char["name"]
    physical_desc = build_physical_description(char)

    # Select appropriate camera and lighting for lane
    if lane == "sfw":
        camera = random.choice(["portrait_studio", "environmental", "fashion"])
        lighting_key = random.choice(["soft_studio", "natural_window", "golden_hour", "bright_airy"])
    elif lane == "suggestive":
        camera = random.choice(["portrait_studio", "environmental", "intimate"])
        lighting_key = random.choice(["natural_window", "golden_hour", "rembrandt"])
    elif lane == "spicy":
        camera = random.choice(["intimate", "portrait_studio"])
        lighting_key = random.choice(["moody_intimate", "rembrandt", "dramatic_shadows"])
    else:  # nsfw
        camera = random.choice(["intimate", "portrait_studio"])
        lighting_key = random.choice(["moody_intimate", "dramatic_shadows", "golden_hour"])

    lighting = LIGHTING_SETUPS[lighting_key]
    clothing = build_clothing_description(char, lane)
    scene = build_scene_description(char, lane, scenario)

    # Bundle narrative context
    narrative = ""
    if bundle_size > 1 and bundle_context:
        if bundle_size == 3:
            positions = ["establishing shot", "progression", "climax/reveal"]
        elif bundle_size == 5:
            positions = ["intro/context", "build-up", "peak moment", "alternative angle", "closing shot"]
        elif bundle_size == 10:
            positions = [
                "establishing wide", "medium context", "close portrait",
                "action/pose 1", "action/pose 2", "detail shot",
                "alternative outfit", "candid moment", "dramatic pose",
                "signature closing"
            ]
        else:
            positions = [f"image {i+1}" for i in range(bundle_size)]

        pos = positions[min(image_index_in_bundle, len(positions) - 1)]
        narrative = (
            f"Bundle theme: {bundle_context}. This is the {pos} "
            f"({image_index_in_bundle + 1} of {bundle_size}). "
        )

    # Composition based on lane and position
    compositions = {
        "sfw": ["portrait", "three-quarter body", "full-body environmental", "candid over-shoulder"],
        "suggestive": ["close-up with bokeh", "three-quarter reclining", "mirror reflection", "over-shoulder look-back"],
        "spicy": ["intimate close-up", "reclining on bed", "kneeling pose", "standing with dramatic shadows"],
        "nsfw": ["artistic figure study", "reclining nude composition", "dramatic silhouette", "intimate overhead view"]
    }
    comp = random.choice(compositions.get(lane, compositions["sfw"]))

    prompt = (
        f"Subject: {name}, a {char['age']}-year-old {char['ethnicity']} woman "
        f"with {char['heritage']} heritage. "
        f"Physical: {physical_desc} "
        f"Scene: {scene}. {narrative}"
        f"She is {clothing}. "
        f"Composition: {comp} composition. "
        f"Expression: {char['personality']['expression_default']}. "
        f"Personality energy: {char['personality']['vibe']}. "
        f"Lighting: {lighting} "
        f"{build_technical_block(camera)} "
        f"{build_quality_requirements()}"
    )
    return prompt


# ---------------------------------------------------------------------------
# Batch Generators
# ---------------------------------------------------------------------------
def generate_all_master_prompts() -> dict:
    """Generate all master image prompts (3 per character, 63 total)."""
    chars = load_characters()
    results = {}
    for char_id, char in chars.items():
        results[char_id] = {
            "name": char["name"],
            "front": {
                "prompt": generate_master_prompt(char, "front"),
                "negative": generate_master_negative_prompt(char),
                "filename": f"{char_id}_face_01.png"
            },
            "angle": {
                "prompt": generate_master_prompt(char, "angle"),
                "negative": generate_master_negative_prompt(char),
                "filename": f"{char_id}_face_02.png"
            },
            "natural": {
                "prompt": generate_master_prompt(char, "natural"),
                "negative": generate_master_negative_prompt(char),
                "filename": f"{char_id}_face_03.png"
            }
        }
    return results


def generate_vault_manifest(char_id: str, seed_base: int = 42) -> dict:
    """
    Generate the complete vault manifest for a single character.
    Returns structured data for all 4 lanes x 200 images = 800 images.
    """
    chars = load_characters()
    lanes_config = load_lanes()
    char = chars[char_id]
    manifest = {
        "character": char["name"],
        "character_id": char_id,
        "total_images": 0,
        "lanes": {}
    }

    random.seed(seed_base + hash(char_id))

    for lane_key in ["sfw", "suggestive", "spicy", "nsfw"]:
        lane_config = lanes_config["lanes"][lane_key]
        dist = lane_config["distribution"]
        lane_images = []

        # --- One-off images ---
        for i in range(dist["one_off"]):
            prompt_data = {
                "type": "one_off",
                "index": i + 1,
                "prompt": generate_vault_prompt(char, lane_key),
                "negative": generate_master_negative_prompt(char),
                "filename": f"{char_id}_{lane_key}_oneoff_{i+1:03d}.png",
                "seed": seed_base + i
            }
            lane_images.append(prompt_data)

        # --- 3-image bundles ---
        bundle_themes_3 = [
            "getting ready for a night out",
            "morning routine at home",
            "casual day exploration",
            "relaxing evening wind-down",
            "fitness and wellness session",
            "outfit try-on session",
            "coffee shop hangout",
            "sunset golden hour series",
            "behind the scenes moments",
            "seasonal vibe check"
        ]
        for b in range(dist["bundle_3"]["count"]):
            theme = bundle_themes_3[b % len(bundle_themes_3)]
            for img in range(dist["bundle_3"]["per_bundle"]):
                prompt_data = {
                    "type": "bundle_3",
                    "bundle_index": b + 1,
                    "image_in_bundle": img + 1,
                    "bundle_theme": theme,
                    "prompt": generate_vault_prompt(
                        char, lane_key,
                        bundle_context=theme,
                        image_index_in_bundle=img,
                        bundle_size=3
                    ),
                    "negative": generate_master_negative_prompt(char),
                    "filename": f"{char_id}_{lane_key}_b3_{b+1:02d}_{img+1:02d}.png",
                    "seed": seed_base + 1000 + b * 10 + img
                }
                lane_images.append(prompt_data)

        # --- 5-image bundles ---
        bundle_themes_5 = [
            "a day in my life",
            "weekend getaway adventure",
            "behind the scenes photoshoot",
            "seasonal collection",
            "date night preparation",
            "home comfort session",
            "outdoor adventure series",
            "self-care ritual",
            "new outfit showcase",
            "birthday celebration vibes"
        ]
        for b in range(dist["bundle_5"]["count"]):
            theme = bundle_themes_5[b % len(bundle_themes_5)]
            for img in range(dist["bundle_5"]["per_bundle"]):
                prompt_data = {
                    "type": "bundle_5",
                    "bundle_index": b + 1,
                    "image_in_bundle": img + 1,
                    "bundle_theme": theme,
                    "prompt": generate_vault_prompt(
                        char, lane_key,
                        bundle_context=theme,
                        image_index_in_bundle=img,
                        bundle_size=5
                    ),
                    "negative": generate_master_negative_prompt(char),
                    "filename": f"{char_id}_{lane_key}_b5_{b+1:02d}_{img+1:02d}.png",
                    "seed": seed_base + 2000 + b * 10 + img
                }
                lane_images.append(prompt_data)

        # --- 10-image bundles ---
        bundle_themes_10 = [
            "complete professional photoshoot",
            "themed fantasy collection",
            "location discovery series",
            "transformation and evolution set"
        ]
        for b in range(dist["bundle_10"]["count"]):
            theme = bundle_themes_10[b % len(bundle_themes_10)]
            for img in range(dist["bundle_10"]["per_bundle"]):
                prompt_data = {
                    "type": "bundle_10",
                    "bundle_index": b + 1,
                    "image_in_bundle": img + 1,
                    "bundle_theme": theme,
                    "prompt": generate_vault_prompt(
                        char, lane_key,
                        bundle_context=theme,
                        image_index_in_bundle=img,
                        bundle_size=10
                    ),
                    "negative": generate_master_negative_prompt(char),
                    "filename": f"{char_id}_{lane_key}_b10_{b+1:02d}_{img+1:02d}.png",
                    "seed": seed_base + 3000 + b * 20 + img
                }
                lane_images.append(prompt_data)

        manifest["lanes"][lane_key] = {
            "total": len(lane_images),
            "images": lane_images
        }
        manifest["total_images"] += len(lane_images)

    return manifest


# ---------------------------------------------------------------------------
# File Output Helpers
# ---------------------------------------------------------------------------
def export_master_prompts_to_files(output_dir: str = None):
    """Export master prompts to text files for ComfyUI consumption."""
    if output_dir is None:
        output_dir = str(BASE_DIR / "output" / "master_prompts")
    os.makedirs(output_dir, exist_ok=True)

    all_prompts = generate_all_master_prompts()

    # Per-character files
    for char_id, data in all_prompts.items():
        filepath = os.path.join(output_dir, f"{char_id}_master_prompts.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {data['name']} - Master Reference Prompts\n")
            f.write(f"# Character: {char_id}\n")
            f.write("=" * 70 + "\n\n")
            for pose in ["front", "angle", "natural"]:
                p = data[pose]
                f.write(f"### {pose.upper()} | {p['filename']} ###\n")
                f.write(f"PROMPT:\n{p['prompt']}\n\n")
                f.write(f"NEGATIVE:\n{p['negative']}\n\n")
                f.write("=" * 70 + "\n\n")

    # Consolidated files for batch workflow
    for pose in ["front", "angle", "natural"]:
        filepath = os.path.join(output_dir, f"batch_{pose}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            for char_id, data in all_prompts.items():
                f.write(data[pose]["prompt"] + "\n")

    print(f"Master prompts exported to {output_dir}")
    print(f"  - {len(all_prompts)} character files")
    print(f"  - 3 batch files (front, angle, natural)")
    return output_dir


def export_vault_manifest(char_id: str, output_dir: str = None, seed: int = 42):
    """Export vault manifest for a character to JSON and prompt files."""
    if output_dir is None:
        output_dir = str(BASE_DIR / "output" / "vault_manifests")
    os.makedirs(output_dir, exist_ok=True)

    manifest = generate_vault_manifest(char_id, seed)

    # Save full manifest as JSON
    json_path = os.path.join(output_dir, f"{char_id}_vault_manifest.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Save per-lane prompt files for ComfyUI batch processing
    for lane_key, lane_data in manifest["lanes"].items():
        prompts_path = os.path.join(output_dir, f"{char_id}_{lane_key}_prompts.txt")
        with open(prompts_path, "w", encoding="utf-8") as f:
            for img in lane_data["images"]:
                f.write(img["prompt"] + "\n")

    print(f"Vault manifest for {manifest['character']} ({char_id}):")
    print(f"  Total images: {manifest['total_images']}")
    for lane_key, lane_data in manifest["lanes"].items():
        print(f"  {lane_key}: {lane_data['total']} images")

    return manifest


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Influencer Prompt Engine")
    parser.add_argument("command", choices=["master", "vault", "vault-all", "test"],
                        help="Command to run")
    parser.add_argument("--char", type=str, help="Character ID (e.g., char_001)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", type=str, help="Output directory")

    args = parser.parse_args()

    if args.command == "master":
        export_master_prompts_to_files(args.output)

    elif args.command == "vault":
        if not args.char:
            parser.error("--char required for vault command")
        export_vault_manifest(args.char, args.output, args.seed)

    elif args.command == "vault-all":
        chars = load_characters()
        for char_id in chars:
            export_vault_manifest(char_id, args.output, args.seed)

    elif args.command == "test":
        # Quick test: generate and display a sample prompt
        chars = load_characters()
        print("=" * 70)
        print("PROMPT ENGINE TEST")
        print("=" * 70)

        # Test master prompts for first 3 characters
        for char_id in list(chars.keys())[:3]:
            char = chars[char_id]
            print(f"\n{'='*70}")
            print(f"CHARACTER: {char['name']} ({char_id})")
            print(f"{'='*70}")
            prompt = generate_master_prompt(char, "front")
            print(f"\nFRONT PROMPT ({len(prompt.split())} words):")
            print(prompt[:500] + "...")
            print(f"\nNEGATIVE:")
            print(generate_master_negative_prompt(char))

        # Test vault prompt
        print(f"\n{'='*70}")
        print("VAULT PROMPT SAMPLE")
        print(f"{'='*70}")
        char = chars["char_001"]
        for lane in ["sfw", "suggestive", "spicy", "nsfw"]:
            prompt = generate_vault_prompt(char, lane)
            print(f"\n{lane.upper()} ({len(prompt.split())} words):")
            print(prompt[:300] + "...")
