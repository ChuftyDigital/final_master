#!/usr/bin/env python3
"""
AI Influencer Prompt Engine v3.0
================================
Narrative-style prompt generation optimized for Z-Image Base (6B parameter model).

Z-Image Base responds best to descriptive, storytelling prompts with specific
camera/lighting terminology rather than keyword lists. This engine generates
flowing, cinematic prose that leverages the model's strengths.

Key v3.0 changes from v2.0:
  - Narrative prose style (not keyword lists)
  - Coherent outfit assembly (not random items)
  - Makeup and grooming details included
  - Lighting matched to actual setting/environment
  - Character-specific atmosphere and personality in every prompt
  - Fixed negative prompt logic (no self-contradictions)
  - Niche-specific scenarios for ALL 21 character niches
  - Z-Image Base optimized (CFG 3-7, 30-50 steps, DPM++ 2M Karras)
"""

import json
import os
import random
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CHARACTERS_FILE = BASE_DIR / "characters" / "personas.json"
LANES_FILE = BASE_DIR / "config" / "content_lanes.json"

# ---------------------------------------------------------------------------
# Camera & Technical Presets (narrative format for Z-Image Base)
# ---------------------------------------------------------------------------
CAMERA_PRESETS = {
    "portrait_85mm": (
        "Shot on a Sony A7R V with a Sony FE 85mm f/1.4 GM lens at f/1.8, "
        "ISO 100, 1/200s. The shallow depth of field creates creamy bokeh that "
        "isolates the subject with razor-sharp focus on the eyes. White balance "
        "set to 5600K daylight. Medium format detail rendering at 8K resolution "
        "captures individual hair strands, visible skin pores, and subtle "
        "imperfections that make the image indistinguishable from a real photograph."
    ),
    "portrait_50mm": (
        "Shot on a Canon EOS R5 Mark II with a Canon RF 50mm f/1.2L USM at f/2.0, "
        "ISO 100, 1/160s. The 50mm focal length provides natural perspective "
        "without distortion, mimicking how the human eye perceives a face. "
        "Shallow depth of field softly separates subject from background. "
        "8K resolution with subsurface scattering visible in the skin."
    ),
    "environmental_35mm": (
        "Shot on a Canon EOS R5 Mark II with a Canon RF 35mm f/1.4L VCM at f/2.8, "
        "ISO 200, 1/250s. The wider focal length captures environmental context "
        "while maintaining a natural, undistorted perspective on the subject. "
        "Moderate depth of field keeps the subject sharp while rendering the "
        "background with gentle bokeh. 8K resolution with fine detail throughout."
    ),
    "intimate_85mm": (
        "Shot on a Nikon Z9 with a Nikkor Z 85mm f/1.2 S at f/1.4, ISO 400, "
        "1/125s. The wide aperture creates an extremely shallow depth of field "
        "that wraps the subject in soft focus, drawing attention to the eyes and "
        "expression. The slightly elevated ISO captures warm ambient light without "
        "flash, preserving the intimate atmosphere. Warm 3800K white balance "
        "enhances skin tones."
    ),
    "fashion_medium": (
        "Shot on a Hasselblad X2D 100C medium format with XCD 80mm f/1.9 at f/2.0, "
        "ISO 64, 1/160s. The medium format sensor delivers extraordinary tonal "
        "gradation and color depth with virtually no noise. The rendering has "
        "the distinctive three-dimensional quality unique to medium format, "
        "with micro-contrast that separates every texture and material. "
        "Ultra-high resolution captures fabric weave and skin micro-texture."
    )
}

# ---------------------------------------------------------------------------
# Lighting Setups (narrative format matched to settings)
# ---------------------------------------------------------------------------
LIGHTING_SETUPS = {
    "soft_studio": (
        "Lit by a large octagonal softbox positioned 45 degrees from camera "
        "axis and slightly above eye level, with a white reflector below the chin "
        "providing gentle fill. The light wraps around the face, eliminating harsh "
        "shadows while preserving the natural dimensionality of the features. "
        "Color temperature calibrated to 5600K daylight, rendering skin tones "
        "with clinical accuracy."
    ),
    "rembrandt": (
        "Rembrandt lighting with the key light at 45 degrees to the subject's "
        "left, elevated 30 degrees above eye level. The characteristic triangular "
        "highlight appears on the shadow-side cheek, sculpting the face with "
        "dramatic dimensionality. A silver reflector provides controlled fill at "
        "a 2:1 ratio, and a subtle hair light from behind creates separation "
        "and a luminous rim along the hair."
    ),
    "golden_hour_outdoor": (
        "Natural golden hour sunlight streaming at a low angle, bathing everything "
        "in warm amber tones with long, soft shadows. The backlit quality creates "
        "a natural rim light effect that outlines the hair and shoulders with a "
        "golden halo. Warm surfaces nearby reflect fill light back into the face, "
        "preventing shadow detail loss while maintaining the romantic atmosphere."
    ),
    "window_natural": (
        "Soft directional light from a large window to camera-left, diffused "
        "through sheer curtains into gentle, wrapping illumination. The room's "
        "ambient warmth provides subtle fill on the shadow side. The quality "
        "is reminiscent of a painter's north-facing studio - even, flattering, "
        "and revealing of fine skin texture without harshness."
    ),
    "moody_warm": (
        "Low-key lighting from a single warm source to one side, creating deep "
        "shadows and an intimate atmosphere. Warm practicals in frame - candles, "
        "a table lamp - add depth and pools of light. The 3200K color temperature "
        "renders skin in rich, warm tones that feel sensual and inviting."
    ),
    "dramatic_chiaroscuro": (
        "High-contrast chiaroscuro lighting with a focused key from above-left, "
        "carving dramatic shadows that sculpt bone structure and musculature. "
        "Minimal fill allows deep, rich blacks for a Renaissance-painting quality. "
        "A subtle rim light creates striking edge definition against the dark "
        "background, separating the subject from shadow."
    ),
    "bright_editorial": (
        "Bright, clean editorial lighting from multiple diffused sources - two "
        "large softboxes at 45 degrees with a beauty dish overhead. Fill "
        "reflectors minimize shadows for a fresh, modern commercial look. "
        "5800K slightly cool balance gives a crisp, contemporary feel."
    ),
    "neon_rgb": (
        "Colorful ambient LED lighting creating vibrant color washes from "
        "multiple angles. RGB strip lights paint the scene in electric blues, "
        "purples, and pinks. The mixed color temperatures create a modern, "
        "energetic atmosphere characteristic of gaming setups and nightlife."
    ),
    "dark_atmospheric": (
        "Atmospheric low-key lighting dominated by deep shadows and selective "
        "illumination. A single focused light source creates pools of visibility "
        "against near-darkness. Rim light traces the contours of the body. "
        "The mood is gothic, powerful, and deliberately theatrical."
    ),
    "tropical_sun": (
        "Bright tropical sunlight filtered through palm fronds, creating dappled "
        "patterns of light and shadow across the skin. The intense overhead sun "
        "is softened by natural diffusion, while reflected light from sand or "
        "water fills shadows from below. High color saturation captures the "
        "vivid greens and blues of the tropical setting."
    )
}

# ---------------------------------------------------------------------------
# Character-Specific Outfit Builder
# ---------------------------------------------------------------------------
OUTFIT_SETS = {
    "sfw": {
        "Beach/Bikini Lifestyle": [
            "a flowing white sundress with thin straps, barefoot with a delicate gold anklet",
            "high-waisted denim shorts and a cropped linen top, hair pulled up casually",
            "a colorful maxi dress with tropical print, simple sandals, gold hoop earrings",
            "athletic swimwear one-piece covered by an open button-up shirt, beach casual"
        ],
        "Equestrian/Country Elite": [
            "tailored cream riding breeches with tall leather boots, a fitted navy blazer over a white silk blouse",
            "an elegant tweed skirt suit with pearl earrings, standing with aristocratic poise",
            "a Barbour waxed jacket over a cashmere turtleneck, with riding gloves tucked in pocket",
            "a flowing silk blouse tucked into high-waisted trousers, Hermes scarf at the neck"
        ],
        "Luxury Travel/Aviation": [
            "a perfectly pressed flight attendant uniform with silk scarf, polished and professional",
            "an elegant wrap dress in deep navy with subtle gold jewelry, travel-ready chic",
            "a tailored blazer over a silk camisole with designer trousers, understated luxury",
            "a cashmere turtleneck with perfectly fitted trousers and designer loafers"
        ],
        "Gaming/E-Sports (Cute/Casual)": [
            "an oversized anime graphic tee hanging off one shoulder, paired with cute shorts",
            "a cozy hoodie with cat ears on the hood, paired with knee-high socks",
            "a gaming jersey with her team name, casual leggings, LED cat-ear headband on",
            "cute pajama set with cartoon print, fuzzy slippers, gaming headset around neck"
        ],
        "Fitness/Athletic Training": [
            "a sports bra and high-waisted leggings in coordinating colors, training shoes",
            "a fitted tank top and compression shorts, hair in a high braided ponytail",
            "a zip-up athletic jacket over a sports bra, with boxing wraps on hands",
            "moisture-wicking running outfit, fitness watch, wireless earbuds visible"
        ],
        "Cosplay/Anime": [
            "a cute Japanese street-fashion outfit - layered skirt, platform boots, hair clips",
            "a school-uniform-inspired outfit with pleated skirt and knee socks",
            "a kawaii pastel coordinate with lace details and platform shoes",
            "a colorful harajuku-style layered outfit with matching hair accessories"
        ],
        "Fashion/Haute Couture": [
            "a perfectly tailored little black dress with minimal gold jewelry, classic heels",
            "a structured designer coat over a silk blouse, wide-leg trousers, statement sunglasses",
            "a flowing haute couture gown in rich fabric, hair in an effortless updo",
            "an editorial outfit - deconstructed blazer, architectural skirt, avant-garde accessories"
        ],
        "Amateur/Girl Next Door": [
            "worn-in denim shorts with a fitted band tee, casual sneakers, hair in a messy ponytail",
            "a simple sundress with a denim jacket thrown over, minimal jewelry",
            "flannel shirt tied at the waist over a tank top, cowboy boots, natural and relaxed",
            "a casual college hoodie with leggings, backpack over one shoulder"
        ],
        "MILF/Mature Latina": [
            "an elegant form-fitting wrap dress in a rich jewel tone, gold jewelry",
            "stylish athletic wear that highlights her confident figure, hair swept up",
            "a sophisticated blouse with tailored pants, statement earrings, polished heels",
            "a beautiful flowing dress with Brazilian-inspired patterns"
        ],
        "Yoga/Wellness/Spiritual": [
            "flowing bohemian yoga pants and a crop top, mala beads draped around the wrist",
            "a simple sari-inspired wrap in natural fabric, gold nose ring catching the light",
            "loose linen clothing in earth tones, barefoot, spiritual jewelry",
            "fitted yoga attire - sports bra and leggings in calming earth colors"
        ],
        "Alternative/Tattooed": [
            "a vintage band tee with ripped black jeans and combat boots, full sleeve tattoos visible",
            "a cropped leather jacket over a mesh top, layered chain necklaces, dark lipstick",
            "high-waisted plaid skirt with fishnet tights, Doc Martens, choker necklace",
            "an oversized flannel open over a fitted black tank, nose ring gleaming"
        ],
        "ASMR/Girlfriend Experience": [
            "an oversized cozy sweater that hangs off one shoulder, hair loose and soft",
            "silk pajama set in soft pink, barefoot, looking gentle and approachable",
            "a comfortable cardigan over a simple camisole, hair clips, warm socks",
            "a cute loungewear set, wrapped in a blanket, holding a warm mug"
        ],
        "Dominatrix/BDSM": [
            "a tailored black power suit with dramatic shoulders, black leather choker, commanding presence",
            "an elegant structured black dress with architectural lines, statement rings",
            "a black silk blouse with high-waisted leather trousers, sleek ponytail",
            "a corseted top with tailored pants, thigh-high boots barely visible"
        ],
        "College/Young Adult (18+)": [
            "a university sweater two sizes too big, plaid mini skirt, knee socks",
            "casual jeans and a cropped top, backpack, scrunchie in her red hair",
            "a cute skater dress with a denim jacket, white sneakers, youthful energy",
            "pajama shorts and an oversized sleep shirt, messy bun, studying vibes"
        ],
        "MILF/Cougar": [
            "a casual but flattering beach dress that moves in the wind, simple jewelry",
            "stylish denim cutoffs with a tucked-in linen shirt, sunglasses pushed up in hair",
            "activewear that shows her fit figure - crop top and bike shorts, beach casual",
            "a flowing maxi dress in coastal colors, bare shoulders, effortlessly sexy"
        ],
        "Petite Asian/Feet Content": [
            "an oversized sweater that dwarfs her tiny frame, cute ankle socks, delicate jewelry",
            "a mini skirt with a fitted top, platform shoes adding height, hair ribbons",
            "a cute dress that emphasizes her petite proportions, ballet flats",
            "casual shorts and a crop top, barefoot on hardwood, looking sweet"
        ],
        "Latina Curves/BBW": [
            "a vibrant bodycon dress that celebrates her curves, bold statement earrings",
            "colorful traditional-inspired outfit with embroidery, flowers in her hair",
            "a form-fitting jumpsuit in a rich color, confident and proud stance",
            "high-waisted jeans and a fitted crop top, bold lipstick, gold bangles"
        ],
        "BBW/Southern Charm": [
            "a floral sundress with lace details, pearl necklace, cowboy boots",
            "comfortable but flattering denim and a feminine blouse, sun hat",
            "a soft cotton dress in warm colors, cardigan over shoulders, genuine warmth",
            "cute country-chic outfit - plaid shirt tied at waist, denim skirt"
        ],
        "Black Beauty/Melanin Content": [
            "a stunning African-print wrap dress, gold statement jewelry highlighting melanin",
            "a tailored power suit in a bold color that pops against her dark skin",
            "elegant casual - fitted top with wide-leg pants, African-inspired accessories",
            "a flowing white dress that creates stunning contrast with her rich dark skin"
        ],
        "Lesbian/Couples Content": [
            "casual athletic wear - tank top and board shorts, minimal jewelry, sporty watch",
            "comfortable streetwear - fitted henley, jeans, clean sneakers",
            "a casual button-up with rolled sleeves, slim chinos, confident stance",
            "swim wear - one-piece or sporty bikini, beach-ready and naturally confident"
        ],
        "Sexy Japanese Gamer/Competitive Streaming": [
            "a fitted gaming jersey with her tag, comfortable leggings, gaming headset on",
            "casual streetwear - crop top with high-waisted joggers, sneakers, subtle eyeliner",
            "a cropped hoodie showing midriff, comfortable shorts, hair in a messy bun with red highlights visible",
            "athletic wear - sports bra and fitted shorts for a workout stream, wrist wraps"
        ]
    }
}

# ---------------------------------------------------------------------------
# Makeup Descriptions per Character (from persona data)
# ---------------------------------------------------------------------------
def build_makeup_description(char: dict, lane: str) -> str:
    """Build makeup description that matches the character and lane."""
    base_makeup = char["style"]["makeup"]

    if lane == "sfw":
        return base_makeup
    elif lane == "suggestive":
        return f"{base_makeup}, slightly enhanced with a touch more definition"
    elif lane == "spicy":
        return f"sultry version of her signature look - {base_makeup}, with smoky eye enhancement"
    elif lane == "nsfw":
        return f"minimal makeup highlighting natural features, {base_makeup.split(',')[0]}"
    return base_makeup


# ---------------------------------------------------------------------------
# Physical Description Builder (natural prose, not template)
# ---------------------------------------------------------------------------
def build_physical_description(char: dict) -> str:
    """Build a flowing, natural prose physical description."""
    p = char["physical"]
    name = char["name"]

    # Build as natural prose, not a list
    desc = (
        f"a {char['age']}-year-old {char['ethnicity']} woman of {char['heritage']} heritage, "
        f"standing {p['height']} with {p['build']}. "
        f"Her {p['hair_color']} hair is {p['hair_length']}, {p['hair_texture']}. "
        f"She has {p['eye_color']} eyes, {p['eye_shape']}, set in a face with "
        f"{p['face_shape']}. Her {p['skin_tone']} skin has {p['skin_texture']}, "
        f"with natural texture visible - real pores, subtle imperfections, "
        f"fine vellus hair catching the light"
    )

    if p.get("distinguishing_features"):
        desc += f". {p['distinguishing_features']}"

    return desc


# ---------------------------------------------------------------------------
# Lighting Selector (matches actual setting, not random)
# ---------------------------------------------------------------------------
SETTING_LIGHTING_MAP = {
    # outdoor / beach
    "beach": "golden_hour_outdoor",
    "ocean": "tropical_sun",
    "pool": "tropical_sun",
    "sunset": "golden_hour_outdoor",
    "pier": "golden_hour_outdoor",
    "yacht": "golden_hour_outdoor",
    "outdoor": "golden_hour_outdoor",
    "garden": "golden_hour_outdoor",
    "park": "golden_hour_outdoor",
    "countryside": "golden_hour_outdoor",
    "street": "golden_hour_outdoor",
    "rooftop": "golden_hour_outdoor",
    "boardwalk": "golden_hour_outdoor",
    # indoor warm
    "bedroom": "moody_warm",
    "bathtub": "moody_warm",
    "bath": "moody_warm",
    "candle": "moody_warm",
    "fireplace": "moody_warm",
    "intimate": "moody_warm",
    "cozy": "window_natural",
    "morning": "window_natural",
    # indoor studio
    "studio": "soft_studio",
    "fashion": "bright_editorial",
    "editorial": "bright_editorial",
    # dark / alternative
    "dungeon": "dark_atmospheric",
    "club": "dark_atmospheric",
    "gothic": "dark_atmospheric",
    "dark": "dark_atmospheric",
    "alley": "dramatic_chiaroscuro",
    "underground": "dark_atmospheric",
    "bar": "moody_warm",
    "dive": "moody_warm",
    # gaming / tech
    "gaming": "neon_rgb",
    "rgb": "neon_rgb",
    "led": "neon_rgb",
    "streaming": "neon_rgb",
    # professional
    "library": "window_natural",
    "office": "window_natural",
    "cafe": "window_natural",
    "kitchen": "window_natural",
    "manor": "window_natural",
    "stable": "golden_hour_outdoor",
    # default
    "default": "soft_studio"
}


def select_lighting_for_scene(scene_text: str) -> str:
    """Select lighting that actually matches the described scene."""
    scene_lower = scene_text.lower()
    for keyword, lighting_key in SETTING_LIGHTING_MAP.items():
        if keyword in scene_lower:
            return LIGHTING_SETUPS[lighting_key]
    return LIGHTING_SETUPS["soft_studio"]


# ---------------------------------------------------------------------------
# Negative Prompt Builder (fixed logic)
# ---------------------------------------------------------------------------
def build_negative_prompt(char: dict, lane: str = "sfw") -> str:
    """Generate character-aware negative prompt. Fixed contradictions from v2."""
    base = (
        "cartoon, anime, illustration, painting, drawing, CGI, 3D render, "
        "low quality, blurry, distorted features, multiple people, deformed, "
        "mutation, extra limbs, text, watermark, signature, frame, border, "
        "bad anatomy, unrealistic proportions, different person, inconsistent "
        "features, plastic skin, artificial smoothness, overprocessed, HDR "
        "artifacts, oversaturated, JPEG artifacts, over-sharpened, crunchy texture"
    )

    p = char["physical"]
    negatives = []

    # Hair color negation - only negate colors the character DOESN'T have
    hair = p["hair_color"].lower()
    if "blonde" not in hair and "light" not in hair and "bleach" not in hair:
        negatives.append("blonde hair")
    if "red" not in hair and "auburn" not in hair and "ginger" not in hair:
        negatives.append("red hair, ginger hair")
    if "black" not in hair and "dark" not in hair:
        negatives.append("black hair")
    if "brown" not in hair and "chestnut" not in hair and "dark" not in hair:
        negatives.append("brown hair")

    # Build negation - negate the OPPOSITE of what the character is
    build = p["build"].lower()
    if "petite" in build or "slim" in build or "delicate" in build:
        negatives.append("overweight, heavyset, muscular")
    elif "full" in build or "voluptuous" in build or "curvy" in build:
        negatives.append("skinny, underweight, bony")
    elif "athletic" in build or "muscular" in build or "toned" in build:
        negatives.append("overweight, frail, skinny")

    # Skin tone - negate opposite
    skin = p["skin_tone"].lower()
    if any(w in skin for w in ["dark", "deep", "rich", "melanin", "brown"]):
        negatives.append("pale skin, white skin, light complexion")
    elif any(w in skin for w in ["pale", "fair", "porcelain", "light"]):
        negatives.append("dark skin, deeply tanned")
    elif any(w in skin for w in ["olive", "tan", "golden", "bronze"]):
        negatives.append("pale white skin, very dark skin")

    # Eye color negation
    eyes = p["eye_color"].lower()
    if "blue" not in eyes and "grey" not in eyes and "gray" not in eyes and "ice" not in eyes:
        negatives.append("blue eyes")
    if "brown" not in eyes and "dark" not in eyes and "warm" not in eyes:
        negatives.append("brown eyes")
    if "green" not in eyes:
        negatives.append("green eyes")

    # Lane-specific negatives
    if lane in ("sfw", "suggestive"):
        negatives.append("nudity, explicit, naked")

    return base + ", " + ", ".join(negatives)


# ---------------------------------------------------------------------------
# Character Atmosphere Builder
# ---------------------------------------------------------------------------
def build_atmosphere(char: dict, lane: str) -> str:
    """Build a rich, character-specific atmosphere description."""
    vibe = char["personality"]["vibe"]
    traits = char["personality"]["traits"]
    niche = char["niche"]

    trait_str = " and ".join(traits[:2])

    if lane == "sfw":
        return (
            f"The atmosphere radiates {vibe}. There is a sense of {trait_str} "
            f"energy in every detail - from her posture to the way she occupies "
            f"the space. The image feels like a candid moment captured by a "
            f"photographer who truly understands her {niche.lower()} world."
        )
    elif lane == "suggestive":
        return (
            f"The atmosphere carries an undercurrent of {vibe}, with a playful "
            f"tension between what is shown and what is implied. Her {trait_str} "
            f"nature comes through in the way she holds the camera's gaze. "
            f"The image has the quality of an intimate behind-the-scenes moment."
        )
    elif lane == "spicy":
        return (
            f"The atmosphere is charged with sensual energy rooted in {vibe}. "
            f"Shadows and light play across her form, creating an intimate space "
            f"that feels private and deliberate. Her {trait_str} personality "
            f"intensifies the scene's magnetic pull."
        )
    else:  # nsfw
        return (
            f"The atmosphere is raw and uninhibited, grounded in the authenticity "
            f"of {vibe}. There is nothing artificial about this moment - it "
            f"captures {trait_str} energy with artistic integrity. The lighting "
            f"and composition elevate this beyond explicit into fine-art territory."
        )


# ---------------------------------------------------------------------------
# Niche-Specific Scenarios (ALL 21 niches, not just defaults)
# ---------------------------------------------------------------------------
NICHE_SCENARIOS = {
    "Beach/Bikini Lifestyle": {
        "sfw": [
            "walking barefoot along the Miami shoreline at golden hour, waves lapping at her ankles, windswept hair catching the last sunlight",
            "sitting cross-legged on a beach towel reading a paperback, ocean waves rolling behind her, barefoot and relaxed",
            "leaning against the railing of a seaside pier at sunset, the warm light painting her skin in amber and gold",
            "at a coastal outdoor cafe sipping a fresh coconut, marina boats bobbing in the background",
            "exploring rocky tide pools at low tide, crouched down with curious delight, natural and unposed",
            "jogging along the hard-packed sand at sunrise, ocean spray in the air, athletic and free",
            "sitting on a lifeguard tower at dusk, legs dangling, watching the sunset paint the sky",
            "browsing at an open-air beachside market, testing a shell necklace, easy and natural"
        ],
        "suggestive": [
            "emerging from the turquoise ocean, water cascading down her body, sunlight catching every droplet on her skin",
            "lying on a beach lounger in a bikini, lazily peering over her sunglasses with a flirty half-smile",
            "at a pool party, wet hair slicked back, playfully splashing near the pool edge",
            "applying sunscreen to her sun-warmed shoulders, looking back over her shoulder with an inviting smile",
            "stretching on the beach in fitted activewear at sunrise, body silhouetted against the pink sky",
            "leaning against a yacht railing, wind billowing a sheer sarong around her hips",
            "under a beach shower, eyes closed, water running down her neck, peaceful and sensual",
            "sitting on smooth rocks by the ocean, knees drawn up, wet swimwear clinging to her figure"
        ],
        "spicy": [
            "in a private beach cabana with sheer curtains billowing, wearing a barely-there string bikini, reclining on white cushions",
            "lying on a daybed by an infinity pool, string bikini, one hand behind her head, inviting gaze at the camera",
            "in a beach house bedroom with floor-to-ceiling ocean views, morning light on her lingerie-clad body",
            "standing in an outdoor shower, water cascading over her, wearing minimal swimwear, steam rising",
            "on rumpled silk sheets in a beach house, wearing a delicate lace set, ocean breeze through the curtains",
            "in a private hot tub on a yacht deck, steam curling around her bare shoulders, looking up through wet lashes",
            "lying face-down on a beach towel, bikini top untied, the strings trailing across the sand, looking playfully back",
            "standing in the doorframe of a beach house at sunset, backlit silhouette, a silk robe falling open"
        ],
        "nsfw": [
            "on a private stretch of beach at golden hour, an artistic nude figure study with the warm light sculpting every curve",
            "in a luxury freestanding bathtub overlooking the ocean through panoramic windows, candlelit, partially submerged",
            "lying on white sheets scattered with tropical frangipani flowers, a fine-art nude study in soft morning light",
            "under a private outdoor rainfall shower surrounded by tropical plants, water streaming over her natural form",
            "reclining on a teak chaise by a private plunge pool, nude sunbathing, completely serene expression",
            "in the beach house bedroom, nude on tangled white sheets, ocean-breeze curtains framing the shot",
            "standing at floor-to-ceiling glass overlooking the ocean, full figure silhouetted by sunrise light",
            "floating weightlessly in a calm infinity pool at dawn, minimalist artistic nude composition"
        ]
    },
    "Equestrian/Country Elite": {
        "sfw": [
            "standing beside her horse in a sunlit stable, one hand on the bridle, radiating calm authority",
            "seated in the manor library beside a crackling fire, legs crossed, leather-bound book in hand",
            "walking through the manicured gardens of the estate, autumn leaves drifting, aristocratic poise",
            "at the polo grounds with champagne flute in hand, watching intently, the picture of refined composure",
            "at an antique writing desk in the study, fountain pen in hand, surrounded by old leather and oak",
            "grooming her horse in the stable, jacket removed, sleeves rolled, showing a softer human side",
            "striding across the estate grounds with hunting dogs at heel, Wellington boots, commanding the scene",
            "seated in a country pub with a knowing half-smile, effortlessly elegant even in casual surroundings"
        ],
        "suggestive": [
            "in the stable wearing riding breeches and a fitted silk blouse with the top buttons undone, warm hay-scented air",
            "on a Chesterfield sofa by the fire, silk blouse, legs crossed with deliberate elegance, wine glass in hand",
            "just finished riding, slightly disheveled, hair escaping its pins, flushed cheeks, breathless confidence",
            "at the manor window in a silk robe, morning light streaming in, coffee held to her lips, composed power",
            "descending the manor staircase in a figure-hugging cocktail dress for the country ball, pearl drop earrings",
            "in the tack room, wearing jodhpurs and a corset-style top, riding crop resting against her thigh",
            "lounging in the drawing room in silk pajamas, reading with a glass of red wine, firelight on her skin",
            "standing in the stable doorway, white shirt slightly dampened and clinging, unshakeable confidence"
        ],
        "spicy": [
            "in the master bedroom of the manor, silk lingerie, perched on the edge of a four-poster bed, firelight flickering",
            "wearing a vintage riding corset and silk stockings, seated at the vanity, applying perfume to her wrists",
            "in the deep copper bathtub of the manor bathroom, candlelight dancing on the water and her skin",
            "standing before an ornate gilt mirror, silk robe open, morning light revealing her figure",
            "on a velvet chaise longue in French lace lingerie, fireplace glowing amber behind her",
            "in the stable-adjacent boudoir, riding boots and lingerie only, commanding and unapologetic",
            "on silk sheets wearing only her signature pearl necklace, the embodiment of old-money sensuality",
            "at the vanity table applying crimson lipstick, wearing a sheer negligee, catching her own gaze in the mirror"
        ],
        "nsfw": [
            "an artistic nude on the four-poster bed, draped in silk sheets that pool around her hips, golden firelight",
            "standing before the floor-length mirror in the master suite, full nude figure study lit by warm firelight",
            "emerging from the copper bathtub, water sheeting off her body, candlelight catching every contour",
            "on a fur throw before the roaring fireplace, artistic nude, warm shadows wrapping her form",
            "a classical figure study in the manor's portrait gallery, standing nude in natural light from tall Georgian windows",
            "on the silk chaise in an odalisque pose, Renaissance-painting quality, bare and regal",
            "in the private chamber, standing at the rain-streaked window, backlit nude silhouette against grey English sky",
            "in the walled garden folly at dawn, natural nude, the classical architecture framing her like a living sculpture"
        ]
    },
    "default": {
        "sfw": [
            "in her signature environment, naturally posed, genuine and unforced expression that shows who she really is",
            "sitting comfortably in a favorite spot, engaged with something she loves, completely in her element",
            "standing in a location that defines her world, relaxed but aware, personality radiating through her posture",
            "a candid moment during an everyday activity, caught mid-laugh or mid-thought, real and unposed",
            "environmental portrait where the surroundings tell her story as much as her expression does",
            "walking through her neighborhood, natural movement, the light catching her just right",
            "at her favorite spot, immersed in her hobby or passion, photographed without pretense",
            "morning light catching her during a quiet routine moment, intimate and authentic"
        ],
        "suggestive": [
            "in fitted clothing that follows her figure, leaning against a doorframe with playful confidence",
            "getting ready in front of a mirror, applying finishing touches, caught between private and performance",
            "lounging on a sofa in something fitted and comfortable, relaxed but very aware of the camera",
            "looking back over her shoulder, outfit showing her silhouette, a teasing half-smile",
            "stretching languidly, her clothing shifting to reveal more than intended, completely natural",
            "fresh from a shower, hair still damp, wrapped in a towel at the vanity, soft and unguarded",
            "in a form-fitting dress, seated with legs crossed, one finger tracing the neckline absently",
            "on a bed fully clothed but reclined, scrolling her phone, effortlessly attractive"
        ],
        "spicy": [
            "in lingerie on the bed, warm lamplight, looking up through her lashes with deliberate invitation",
            "on tumbled sheets in intimate wear, fabric half-covering, the line between clothed and not",
            "at the bathroom mirror in bra and underwear, caught in the act of undressing, unselfconscious",
            "silk robe sliding off one shoulder, standing in the bedroom doorway, warm backlight",
            "lying on her stomach in lingerie, chin on folded arms, looking back at the camera with intent",
            "standing in a doorway with dramatic backlight, sheer fabric making her silhouette visible",
            "on luxurious dark bedding in lace lingerie, candlelit, an intimate gaze that holds you",
            "at her vanity in just underwear, candlelight, the ritual of getting undressed"
        ],
        "nsfw": [
            "an artistic nude on white sheets, tasteful positioning, soft directional light sculpting her form",
            "in a deep bathtub, water at mid-body, steam rising, intimate atmosphere, completely at ease",
            "a standing figure study in natural window light, editorial quality, unapologetic and beautiful",
            "reclining nude on dark sheets, one arm above her head, artistic composition with intentional shadow",
            "in the shower, water streaming over her, captured through glass with artistic condensation",
            "overhead perspective on the bed, artistic nude, creative framing that is more art than explicit",
            "silhouetted at a window, full figure, dramatic backlight creating a luminous outline",
            "a private moment of self-appreciation, nude, warm intimate lighting, genuine and tender"
        ]
    }
}

# Map all niches to their scenarios (those not explicitly defined use default)
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
# Core Data Loaders
# ---------------------------------------------------------------------------
def load_characters():
    with open(CHARACTERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {c["id"]: c for c in data["characters"]}


def load_lanes():
    with open(LANES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Outfit Selector
# ---------------------------------------------------------------------------
def select_outfit(char: dict, lane: str) -> str:
    """Select a coherent outfit from the character's niche wardrobe."""
    niche = char["niche"]

    if lane in OUTFIT_SETS and niche in OUTFIT_SETS[lane]:
        outfits = OUTFIT_SETS[lane][niche]
        return random.choice(outfits)

    # Fallback: build from character wardrobe data but as coherent outfit
    style = char["style"]
    clothing = style["typical_clothing"]
    accessories = style["accessories"]

    if lane == "sfw":
        top = random.choice([c for c in clothing if not any(
            w in c.lower() for w in ["lingerie", "bikini", "underwear", "bra", "latex"]
        )] or clothing[:2])
        acc = random.choice(accessories) if accessories else ""
        return f"{top}, paired with {acc}" if acc else top
    elif lane == "suggestive":
        items = [c for c in clothing if any(
            w in c.lower() for w in ["fitted", "form", "tight", "crop", "dress", "bikini"]
        )]
        chosen = random.choice(items) if items else random.choice(clothing)
        return f"a flattering {chosen} that accentuates her {char['physical']['build']}"
    elif lane == "spicy":
        return (
            f"delicate lingerie that complements her {char['physical']['skin_tone']} skin, "
            f"the fine lace and silk catching the light"
        )
    else:  # nsfw
        return "bare skin, natural and unadorned, her body a study in authentic beauty"


# ---------------------------------------------------------------------------
# MASTER IMAGE PROMPTS (Workflow 1)
# ---------------------------------------------------------------------------
def generate_master_prompt(char: dict, pose_type: str = "front") -> str:
    """
    Generate a narrative-style prompt for Z-Image Base master reference generation.
    """
    name = char["name"]
    physical = build_physical_description(char)
    makeup = build_makeup_description(char, "sfw")
    outfit = select_outfit(char, "sfw")
    expression = char["personality"]["expression_default"]

    if pose_type == "front":
        scene_and_pose = (
            f"A classic head-and-shoulders portrait of {name} facing the camera "
            f"directly, shoulders squared to the frame. She is positioned with her "
            f"eyes along the upper third line, the frame capturing from mid-chest "
            f"upward. Her head is straight with minimal tilt, projecting directness "
            f"and quiet confidence. Her expression is {expression}. She wears {outfit}. "
            f"Her makeup is {makeup}."
        )
        lighting = LIGHTING_SETUPS["soft_studio"]
        camera = CAMERA_PRESETS["portrait_85mm"]

    elif pose_type == "angle":
        scene_and_pose = (
            f"An elegant three-quarter portrait of {name} with her body angled "
            f"45 degrees from the camera while her head turns toward the lens, "
            f"creating a dynamic pose that reveals the full structure of her face. "
            f"This angle emphasizes her cheekbones and jawline, adding depth and "
            f"dimensionality. Her shoulders are relaxed with a subtle turn creating "
            f"flowing lines through the frame. Her expression is {expression}. "
            f"She wears {outfit}. Her makeup is {makeup}."
        )
        lighting = LIGHTING_SETUPS["rembrandt"]
        camera = CAMERA_PRESETS["portrait_50mm"]

    elif pose_type == "natural":
        setting = random.choice(char["settings"][:3])
        scene_and_pose = (
            f"An environmental portrait of {name} in {setting}, captured in a "
            f"natural, candid moment that reveals her personality. The composition "
            f"frames her at three-quarter to full body with a shallow depth of field "
            f"that keeps her razor-sharp against a softly blurred setting. "
            f"Environmental details reflect her {char['niche']} world. "
            f"Her expression captures {expression} in an unguarded, authentic moment. "
            f"She wears {outfit}. Her makeup is {makeup}."
        )
        lighting = select_lighting_for_scene(setting)
        camera = CAMERA_PRESETS["environmental_35mm"]
    else:
        raise ValueError(f"Unknown pose_type: {pose_type}")

    atmosphere = build_atmosphere(char, "sfw")

    prompt = (
        f"A masterful portrait photograph of {name}, {physical}. "
        f"{scene_and_pose} "
        f"Lighting: {lighting} "
        f"{camera} "
        f"{atmosphere} "
        f"The skin has realistic subsurface scattering with visible pores and "
        f"natural micro-texture. Individual hair strands catch the light with "
        f"realistic variation. The eyes have depth, catchlights, and the subtle "
        f"moisture of a living person. This photograph is indistinguishable from "
        f"one captured by a master portrait photographer - no artificial smoothness, "
        f"no plastic quality, only authentic human beauty rendered with "
        f"technical excellence."
    )
    return prompt


# ---------------------------------------------------------------------------
# VAULT IMAGE PROMPTS (Workflow 2)
# ---------------------------------------------------------------------------
def generate_vault_prompt(
    char: dict,
    lane: str,
    scenario: str = None,
    bundle_context: str = None,
    image_index_in_bundle: int = 0,
    bundle_size: int = 1
) -> str:
    """Generate a narrative-style vault prompt for Z-Image Base."""
    name = char["name"]
    physical = build_physical_description(char)
    makeup = build_makeup_description(char, lane)
    outfit = select_outfit(char, lane)

    # Scene selection
    niche = char["niche"]
    scenarios = NICHE_SCENARIOS.get(niche, NICHE_SCENARIOS["default"])
    lane_scenarios = scenarios.get(lane, scenarios.get("sfw", []))

    if scenario:
        scene = scenario
    elif lane_scenarios:
        scene = random.choice(lane_scenarios)
    else:
        setting = random.choice(char["settings"])
        scene = f"in {setting}, natural and authentic to her character"

    # Lighting matched to the actual scene
    lighting = select_lighting_for_scene(scene)

    # Camera matched to lane
    if lane == "sfw":
        camera = random.choice([
            CAMERA_PRESETS["portrait_85mm"],
            CAMERA_PRESETS["environmental_35mm"],
            CAMERA_PRESETS["fashion_medium"]
        ])
    elif lane == "suggestive":
        camera = random.choice([
            CAMERA_PRESETS["portrait_85mm"],
            CAMERA_PRESETS["portrait_50mm"],
            CAMERA_PRESETS["environmental_35mm"]
        ])
    elif lane == "spicy":
        camera = random.choice([
            CAMERA_PRESETS["intimate_85mm"],
            CAMERA_PRESETS["portrait_85mm"]
        ])
    else:
        camera = random.choice([
            CAMERA_PRESETS["intimate_85mm"],
            CAMERA_PRESETS["portrait_50mm"]
        ])

    # Bundle narrative context
    narrative = ""
    if bundle_size > 1 and bundle_context:
        if bundle_size == 3:
            positions = [
                "the opening shot that sets the scene and mood",
                "the progression where the energy deepens and intensifies",
                "the climactic moment that delivers the emotional peak"
            ]
        elif bundle_size == 5:
            positions = [
                "the introduction, establishing context and character",
                "the build-up, energy beginning to shift and deepen",
                "the peak moment, the emotional and visual climax",
                "an alternative angle, revealing a new perspective",
                "the closing shot, a signature farewell moment"
            ]
        elif bundle_size == 10:
            positions = [
                "a wide establishing shot setting the full scene",
                "a medium shot providing context and body language",
                "a close portrait focusing on expression and eyes",
                "a dynamic action or pose showing movement and energy",
                "a second dynamic pose, different angle and energy",
                "a detail shot capturing texture, skin, or accessory",
                "an alternative outfit or state, showing transformation",
                "a candid moment, caught between poses, real and raw",
                "a dramatic final pose with peak intensity",
                "a signature closing shot that captures her essence"
            ]
        else:
            positions = [f"image {i+1} in the series" for i in range(bundle_size)]

        pos = positions[min(image_index_in_bundle, len(positions) - 1)]
        narrative = f"This is {pos} in a {bundle_size}-image set themed '{bundle_context}'. "

    atmosphere = build_atmosphere(char, lane)

    prompt = (
        f"A photograph of {name}, {physical}. "
        f"Scene: {scene}. {narrative}"
        f"She wears {outfit}. Her makeup is {makeup}. "
        f"Her expression is {char['personality']['expression_default']}. "
        f"Lighting: {lighting} "
        f"{camera} "
        f"{atmosphere} "
        f"Photorealistic quality with natural skin texture showing real pores "
        f"and subsurface scattering. Individual hair strands with natural variation. "
        f"Eyes with depth and realistic catchlights. Indistinguishable from a "
        f"real photograph by a professional photographer."
    )
    return prompt


# ---------------------------------------------------------------------------
# Batch Generators
# ---------------------------------------------------------------------------
def generate_all_master_prompts() -> dict:
    chars = load_characters()
    results = {}
    for char_id, char in chars.items():
        results[char_id] = {
            "name": char["name"],
            "front": {
                "prompt": generate_master_prompt(char, "front"),
                "negative": build_negative_prompt(char, "sfw"),
                "filename": f"{char_id}_face_01.png"
            },
            "angle": {
                "prompt": generate_master_prompt(char, "angle"),
                "negative": build_negative_prompt(char, "sfw"),
                "filename": f"{char_id}_face_02.png"
            },
            "natural": {
                "prompt": generate_master_prompt(char, "natural"),
                "negative": build_negative_prompt(char, "sfw"),
                "filename": f"{char_id}_face_03.png"
            }
        }
    return results


def generate_vault_manifest(char_id: str, seed_base: int = 42) -> dict:
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

        for i in range(dist["one_off"]):
            lane_images.append({
                "type": "one_off", "index": i + 1,
                "prompt": generate_vault_prompt(char, lane_key),
                "negative": build_negative_prompt(char, lane_key),
                "filename": f"{char_id}_{lane_key}_oneoff_{i+1:03d}.png",
                "seed": seed_base + i
            })

        bundle_themes_3 = [
            "getting ready for a night out", "morning routine at home",
            "casual day exploration", "relaxing evening wind-down",
            "fitness and wellness session", "outfit try-on session",
            "coffee shop hangout", "sunset golden hour series",
            "behind the scenes moments", "seasonal vibe check"
        ]
        for b in range(dist["bundle_3"]["count"]):
            theme = bundle_themes_3[b % len(bundle_themes_3)]
            for img in range(dist["bundle_3"]["per_bundle"]):
                lane_images.append({
                    "type": "bundle_3", "bundle_index": b+1,
                    "image_in_bundle": img+1, "bundle_theme": theme,
                    "prompt": generate_vault_prompt(char, lane_key,
                        bundle_context=theme, image_index_in_bundle=img, bundle_size=3),
                    "negative": build_negative_prompt(char, lane_key),
                    "filename": f"{char_id}_{lane_key}_b3_{b+1:02d}_{img+1:02d}.png",
                    "seed": seed_base + 1000 + b*10 + img
                })

        bundle_themes_5 = [
            "a day in my life", "weekend getaway adventure",
            "behind the scenes photoshoot", "seasonal collection",
            "date night preparation", "home comfort session",
            "outdoor adventure series", "self-care ritual",
            "new outfit showcase", "birthday celebration vibes"
        ]
        for b in range(dist["bundle_5"]["count"]):
            theme = bundle_themes_5[b % len(bundle_themes_5)]
            for img in range(dist["bundle_5"]["per_bundle"]):
                lane_images.append({
                    "type": "bundle_5", "bundle_index": b+1,
                    "image_in_bundle": img+1, "bundle_theme": theme,
                    "prompt": generate_vault_prompt(char, lane_key,
                        bundle_context=theme, image_index_in_bundle=img, bundle_size=5),
                    "negative": build_negative_prompt(char, lane_key),
                    "filename": f"{char_id}_{lane_key}_b5_{b+1:02d}_{img+1:02d}.png",
                    "seed": seed_base + 2000 + b*10 + img
                })

        bundle_themes_10 = [
            "complete professional photoshoot", "themed fantasy collection",
            "location discovery series", "transformation and evolution set"
        ]
        for b in range(dist["bundle_10"]["count"]):
            theme = bundle_themes_10[b % len(bundle_themes_10)]
            for img in range(dist["bundle_10"]["per_bundle"]):
                lane_images.append({
                    "type": "bundle_10", "bundle_index": b+1,
                    "image_in_bundle": img+1, "bundle_theme": theme,
                    "prompt": generate_vault_prompt(char, lane_key,
                        bundle_context=theme, image_index_in_bundle=img, bundle_size=10),
                    "negative": build_negative_prompt(char, lane_key),
                    "filename": f"{char_id}_{lane_key}_b10_{b+1:02d}_{img+1:02d}.png",
                    "seed": seed_base + 3000 + b*20 + img
                })

        manifest["lanes"][lane_key] = {"total": len(lane_images), "images": lane_images}
        manifest["total_images"] += len(lane_images)

    return manifest


# ---------------------------------------------------------------------------
# File Output Helpers
# ---------------------------------------------------------------------------
def export_master_prompts_to_files(output_dir: str = None):
    if output_dir is None:
        output_dir = str(BASE_DIR / "output" / "master_prompts")
    os.makedirs(output_dir, exist_ok=True)
    all_prompts = generate_all_master_prompts()

    for char_id, data in all_prompts.items():
        filepath = os.path.join(output_dir, f"{char_id}_master_prompts.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {data['name']} - Master Reference Prompts (Z-Image Base v3.0)\n")
            f.write(f"# Character: {char_id}\n")
            f.write(f"# Model: Z-Image Base | Steps: 40 | CFG: 4.5 | Sampler: DPM++ 2M Karras\n")
            f.write("=" * 70 + "\n\n")
            for pose in ["front", "angle", "natural"]:
                p = data[pose]
                f.write(f"### {pose.upper()} | {p['filename']} ###\n")
                f.write(f"PROMPT:\n{p['prompt']}\n\n")
                f.write(f"NEGATIVE:\n{p['negative']}\n\n")
                f.write("=" * 70 + "\n\n")

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
    if output_dir is None:
        output_dir = str(BASE_DIR / "output" / "vault_manifests")
    os.makedirs(output_dir, exist_ok=True)
    manifest = generate_vault_manifest(char_id, seed)

    json_path = os.path.join(output_dir, f"{char_id}_vault_manifest.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

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
    parser = argparse.ArgumentParser(description="AI Influencer Prompt Engine v3.0")
    parser.add_argument("command", choices=["master", "vault", "vault-all", "test"])
    parser.add_argument("--char", type=str, help="Character ID (e.g., char_001)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str)
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
        chars = load_characters()
        print("=" * 70)
        print("PROMPT ENGINE v3.0 TEST - Z-Image Base Narrative Style")
        print("=" * 70)
        # Test 3 very different characters
        test_chars = ["char_001", "char_011", "char_013"]
        for char_id in test_chars:
            char = chars[char_id]
            print(f"\n{'='*70}")
            print(f"CHARACTER: {char['name']} ({char_id}) - {char['niche']}")
            print(f"{'='*70}")
            for pose in ["front", "angle", "natural"]:
                prompt = generate_master_prompt(char, pose)
                words = len(prompt.split())
                print(f"\n{pose.upper()} ({words} words):")
                print(prompt)
                print()
            neg = build_negative_prompt(char, "sfw")
            print(f"NEGATIVE: {neg}")

        print(f"\n{'='*70}")
        print("VAULT PROMPT COMPARISON (Isabella - all 4 lanes)")
        print(f"{'='*70}")
        char = chars["char_001"]
        for lane in ["sfw", "suggestive", "spicy", "nsfw"]:
            prompt = generate_vault_prompt(char, lane)
            print(f"\n{lane.upper()} ({len(prompt.split())} words):")
            print(prompt)
