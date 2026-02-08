"""
Cinema-Grade Prompt Engine for Z-Image / Lumina2 Models

Generates ultra-detailed natural language prompts (3000-4000+ chars)
optimized for Z-Image's semantic understanding.

Z-Image reads prompts like camera direction — full sentences with
spatial relationships, not SD-style tag spam.

Based on the original Super Factory premium prompt system.
"""

import random
from typing import Any, Dict, List, Optional

from superfactory.models.persona import Persona


class PromptEngine:
    """Generates cinema-grade prompts from persona data."""

    def __init__(self, templates_dir: Optional[str] = None):
        self._templates: Dict[str, Any] = {}

    # ── Hair detail expansions ──────────────────────────────────────

    HAIR_LENGTH_DETAIL = {
        "Long": "cascading down past her shoulders, flowing naturally with subtle movement and catching highlights that reveal dimensional color",
        "Medium": "flowing gracefully around her shoulders with soft natural movement, framing her face with effortless elegance",
        "Short": "styled elegantly and framing her face with modern sophistication, drawing attention to her bone structure",
    }

    EYE_COLOR_DETAIL = {
        "Brown": "deep and expressive with warm undertones that shift between rich chocolate and golden amber in the light",
        "Blue": "vivid and striking with crystalline clarity, shifting between deep sapphire and pale ice depending on the light",
        "Green": "vibrant and captivating with jewel-like intensity, flecked with subtle gold near the pupil",
        "Hazel": "multifaceted with golden and green flecks that shift mesmerizingly in different lighting",
        "Amber": "warm and luminous with honey-golden depths that seem to glow from within",
        "Gray": "cool and penetrating with silver undertones and subtle blue-gray depth",
        "Dark Brown": "intensely dark and expressive with warm mahogany undertones that catch the light beautifully",
    }

    SKIN_TONE_DETAIL = {
        "Warm olive": "a warm olive complexion that glows with natural radiance and health, showing beautiful undertones of gold and bronze",
        "Porcelain": "porcelain skin with delicate, almost translucent quality, showing natural pink undertones and fine texture",
        "Caramel": "a rich caramel skin tone that radiates warmth and vitality, with beautiful golden undertones that catch the light",
        "Bronze": "a stunning bronze complexion that catches the light beautifully, with warm copper undertones and healthy luminosity",
        "Fair": "fair, luminous skin with natural warmth, showing subtle rosy undertones and fine, even texture",
        "Golden": "golden-toned skin that glows with natural warmth, catching light beautifully with honey undertones",
        "Deep brown": "rich deep brown skin with beautiful warm undertones, showing extraordinary luminosity and even texture",
        "Tan": "sun-kissed tan skin with warm golden undertones, radiating health and natural vitality",
        "Ivory": "ivory skin with delicate, refined texture, showing subtle pink warmth and natural luminosity",
        "Light brown": "light brown skin with warm honey undertones, glowing with natural health and beautiful even texture",
    }

    # ── Lighting rigs per pose (from original premium generator) ────

    LIGHTING = {
        "front": (
            "Soft diffused studio lighting setup with a large octagonal softbox "
            "positioned directly in front and slightly above eye level, approximately 45 degrees "
            "from camera axis. A white reflector positioned below chin level provides subtle fill, "
            "eliminating harsh shadows while maintaining natural dimensionality. The key light "
            "creates gentle, flattering illumination that emphasizes cheekbones without creating "
            "deep shadows. Color temperature is calibrated to 5600K daylight balance, ensuring "
            "accurate skin tone reproduction. Background receives minimal light, creating subtle "
            "separation between subject and backdrop."
        ),
        "angle": (
            "Rembrandt-style lighting with key light positioned at 45 degrees to the "
            "subject's left side and elevated 30 degrees above eye level. This creates the "
            "characteristic triangular highlight on the cheek opposite the light source, adding "
            "depth and dimension to the facial structure. A silver reflector on the shadow side "
            "provides controlled fill at approximately 2:1 lighting ratio. A subtle hair light "
            "from behind and above adds separation and dimension to the hair. The lighting sculpts "
            "the face, emphasizing cheekbones and creating a sense of three-dimensionality while "
            "maintaining a flattering, approachable quality."
        ),
        "natural": (
            "Natural window light from a large north-facing window providing soft, "
            "diffused illumination with no harsh shadows. The light wraps around the subject "
            "creating gentle transitions between highlights and shadows. Positioned at approximately "
            "30 degrees from camera axis, the window light creates subtle modeling while maintaining "
            "an authentic, lifestyle feel. A white v-board reflector opposite the window adds soft "
            "fill to shadow areas. The color temperature of 5500K natural daylight renders skin "
            "tones with perfect accuracy. This lighting creates an intimate, approachable atmosphere "
            "that feels genuine and unforced."
        ),
    }

    # ── Camera / technical specs (from original premium generator) ──

    TECHNICAL_SPECS = (
        "Captured with professional-grade equipment using a Sony A7R IV "
        "full-frame mirrorless camera paired with a Zeiss Batis 85mm f/1.8 lens, the gold standard "
        "for portrait photography. The lens is set to f/2.0 to create a beautifully shallow depth "
        "of field that isolates the subject from the background while maintaining tack-sharp focus "
        "on the eyes. ISO is set to 100 for maximum image quality and dynamic range. Shutter speed "
        "is 1/160s to eliminate any motion blur while maintaining natural appearance. "
        "The image is rendered in photorealistic 8K resolution with exceptional detail in every "
        "element — individual strands of hair, the subtle texture of skin with visible pores and "
        "natural imperfections, fine details in fabric and accessories. The color grading maintains "
        "natural skin tones with subtle warmth, professional contrast that adds depth without "
        "looking overprocessed. The background is a smooth, neutral gradient that provides "
        "separation without distraction. Post-processing includes subtle skin retouching that "
        "maintains natural texture while removing temporary blemishes, color correction for accurate "
        "representation, and contrast optimization that enhances depth. The final image has the "
        "quality of a high-end editorial portrait suitable for magazine covers or luxury brand campaigns."
    )

    # ── Composition per pose (from original premium generator) ──────

    COMPOSITION = {
        "front": (
            "Classic head-and-shoulders portrait with {name} positioned squarely facing "
            "the camera, shoulders aligned with the frame. The composition follows the rule of thirds "
            "with eyes positioned along the upper horizontal third line, creating a naturally engaging "
            "focal point. The frame captures from mid-chest upward, providing context while keeping "
            "focus on facial features. Head is straight with minimal tilt, creating a sense of directness "
            "and confidence. Expression is neutral with a soft, natural smile — lips gently closed, "
            "eyes alert and engaged with the camera. This frontal approach creates the most accurate "
            "representation for facial recognition and reference purposes."
        ),
        "angle": (
            "Elegant three-quarter view with {name}'s body at a 45-degree angle to the "
            "camera while head turns back toward the lens, creating a dynamic yet natural pose. This "
            "positioning reveals the full structure of the face while maintaining eye contact with "
            "the viewer. The composition emphasizes cheekbones and jawline through the angular "
            "perspective, adding dimension and visual interest. Shoulders remain relaxed with a subtle "
            "turn that creates elegant lines. Expression features a gentle, engaging smile that "
            "reaches the eyes, creating warmth and approachability. This angle is universally "
            "flattering and provides excellent reference for three-dimensional facial structure."
        ),
        "natural": (
            "Candid-inspired portrait capturing {name} in a relaxed, natural moment. "
            "The pose is asymmetrical and organic, with a slight lean that creates visual interest "
            "without appearing posed. Head is gently tilted, creating a sense of spontaneity and "
            "approachability. The frame captures a three-quarter view that shows personality while "
            "maintaining clarity of features. Expression is warm and genuine with a natural smile "
            "that lights up the face — eyes crinkled slightly at the corners, genuine happiness "
            "evident. This composition prioritizes personality and authenticity, creating an image "
            "that feels like a captured moment rather than a formal portrait, perfect for showing "
            "the subject's natural charisma and warmth."
        ),
    }

    # ── Style / atmosphere per pose ─────────────────────────────────

    ATMOSPHERE = {
        "front": (
            "The image embodies {aesthetic} with a timeless, editorial quality. "
            "The overall mood is sophisticated and confident, conveying professionalism while maintaining "
            "approachability. The aesthetic is clean and modern with subtle luxury undertones. "
            "This is the definitive reference image — the most important of the three for maintaining "
            "consistency across all future generations."
        ),
        "angle": (
            "Capturing {aesthetic} with emphasis on dimensionality and structure. "
            "The mood is engaging and dynamic, showing the subject's charisma from a new perspective. "
            "The aesthetic maintains the luxury feel while adding depth and sophistication. "
            "This angle provides crucial three-dimensional information that helps maintain consistency "
            "when the subject is viewed from different perspectives in generated content."
        ),
        "natural": (
            "Authentic {aesthetic} with emphasis on genuine personality and warmth. "
            "The mood is inviting and approachable, capturing the subject's natural charm. The aesthetic "
            "feels candid and real, as if photographed during a genuine moment of happiness. "
            "This image is essential for showing the subject's personality and ensuring generated "
            "content has emotional authenticity and warmth."
        ),
    }

    CRITICAL_REQUIREMENTS = (
        "This image must show photorealistic quality with natural skin "
        "texture — every pore, fine line, and natural imperfection should be visible. Hair must "
        "appear as individual strands with natural variation. Eyes must have realistic catchlights "
        "and depth. The image should look like it was captured by a master portrait photographer, "
        "not generated by AI. Facial features must be consistent and distinctive, creating a "
        "recognizable individual who maintains their appearance across all three reference images. "
        "No artificial smoothness, no plastic appearance, no exaggerated features — only authentic, "
        "natural beauty captured with technical excellence."
    )

    # ── Bulk generation building blocks ─────────────────────────────

    SHOT_TYPES = [
        "Close-up portrait", "Medium shot", "Three-quarter view",
        "Environmental portrait", "Candid moment", "Mirror selfie",
        "Front camera view", "Over-the-shoulder", "Profile view", "Full body shot",
    ]

    LIGHTING_KEYWORDS = [
        "golden hour sunlight streaming through curtains",
        "soft natural daylight from a large window",
        "warm vanity lighting with subtle catchlights",
        "ring light with visible catchlights in the eyes",
        "soft diffused lighting with no harsh shadows",
        "warm tungsten mixed with natural light",
        "clean studio lighting with neutral background",
        "window light creating soft directional shadows",
        "backlit with warm rim light separating subject from background",
        "overcast outdoor light for soft even illumination",
    ]

    ENVIRONMENT_MARKERS = [
        "aesthetically arranged modern apartment with neutral tones",
        "trendy cafe with warm ambient lighting and cozy atmosphere",
        "rooftop with city skyline blurred in the background",
        "beach at golden hour with soft warm light on skin",
        "luxury hotel room with clean lines and elegant decor",
        "botanical garden with lush greenery creating natural backdrop",
        "urban street with interesting architecture and depth",
        "cozy reading nook bathed in natural light",
        "minimalist studio with smooth neutral backdrop",
        "poolside lounge with tropical atmosphere and warm sunlight",
    ]

    # ── SFW bulk templates (natural sentences, not tags) ────────────

    SFW_TEMPLATES = [
        "{shot} of a {age}-year-old {ethnicity} woman with {hair_desc} and {eye_desc}, {action} in {location}. She wears {outfit}. Her expression is {expression}. {lighting}. Background shows {environment}. {quality}.",
        "{name} posing {pose_style} wearing {outfit}. {location} setting with {bg_style}. {lighting} illuminating her {skin_desc} skin. She has a {expression} expression. {camera}. The overall aesthetic is {aesthetic}.",
        "Professional {photo_style} of {name}, {age}, from {city}. She is {action} in {outfit}. Her {eye_desc} and {hair_desc} frame her face beautifully. {lighting} creating a {mood} atmosphere. {quality}.",
        "{shot} capturing {name} during {action}. She wears {outfit} in {color_palette} tones. {environment}. {lighting} with {color_grading}. {camera}.",
        "Lifestyle moment of {name} {action} at {location}. {outfit_desc}. {expression} look with {eye_contact}. {lighting}. Background features {bg_elements}. {quality}.",
    ]

    SUGGESTIVE_TEMPLATES = [
        "{shot} of {name}, a {age}-year-old {ethnicity} woman, {action} in {location}. She wears {outfit}. Her expression is {expression}. {lighting}. {quality}.",
        "Alluring {photo_style} of {name} in {outfit}, {action} with {mood} energy. {lighting}. Her {skin_desc} skin glows beautifully. {camera}.",
        "Glamorous {shot} of {name} in {location}. {outfit}. {expression}. {lighting} accentuating her {hair_desc} and {eye_desc}. {quality}.",
    ]

    SPICY_TEMPLATES = [
        "Provocative {shot} of {name}, {action} in {location}. {outfit}. Her expression is {expression}. {lighting} accentuating her features. {quality}.",
        "Steamy {photo_style} of {name} in {outfit}. {action}. {lighting}. Her {skin_desc} skin has a beautiful natural glow. {camera}.",
    ]

    NSFW_TEMPLATES = [
        "Intimate {shot} of {name}, {action} in {location}. {outfit}. Her expression is {expression}. {lighting}. {quality}.",
        "Sensual {photo_style} of {name}, {action}. {lighting}. Her {skin_desc} skin catches the light beautifully. {camera}.",
    ]

    # ────────────────────────────────────────────────────────────────
    # Public API
    # ────────────────────────────────────────────────────────────────

    def _physical_description(self, p: Persona) -> str:
        """Build comprehensive physical description from persona data."""
        parts = []

        height = p.height
        body_type = p.build
        parts.append(f"She stands {height} tall with a {body_type}")

        h_color = p.hair_color
        h_length = p.hair_length
        h_texture = p.hair_texture
        h_detail = self.HAIR_LENGTH_DETAIL.get(h_length, self.HAIR_LENGTH_DETAIL["Medium"])
        parts.append(
            f"Her hair is {h_color.lower()} in color, {h_length.lower()} in length and "
            f"{h_texture.lower()} in texture, {h_detail}"
        )

        e_color = p.eye_color
        e_shape = p.eye_shape
        e_detail = self.EYE_COLOR_DETAIL.get(e_color, "striking and expressive")
        parts.append(
            f"Her eyes are {e_color.lower()} and {e_shape.lower()}-shaped, {e_detail}, "
            f"drawing attention with their natural allure"
        )

        skin = p.skin_tone
        skin_detail = self.SKIN_TONE_DETAIL.get(
            skin, f"beautiful {skin.lower()} skin with natural radiance"
        )
        parts.append(f"She has {skin_detail}")

        face_shape = p.face_shape
        if face_shape:
            parts.append(
                f"Her face has an {face_shape.lower()}, creating a naturally photogenic silhouette"
            )

        distinctive = p.distinctive_features
        if distinctive and distinctive.lower() != "unique natural beauty":
            parts.append(f"Notable features include: {distinctive}")

        return ". ".join(parts) + "."

    def reference_prompt(self, persona: Persona, pose: str) -> str:
        """Generate a cinema-grade reference prompt (3000-4000+ chars).

        Replicates the original Super Factory premium prompt quality with
        detailed lighting rigs, camera specs, and photorealism requirements.
        """
        p = persona
        name = p.name
        age = p.age
        ethnicity = p.ethnicity
        nationality = p.nationality
        style_persona = getattr(p, '_data', {}).get("style_persona", {})
        aesthetic = style_persona.get("aesthetic", "sophisticated elegance")
        fashion = style_persona.get("fashion_sense", "elegant contemporary style")
        personality = ""
        if p.personality_summary:
            personality = p.personality_summary.split(".")[0]

        physical = self._physical_description(p)

        sections = [
            (
                f"Subject: Professional portrait photograph of {name}, a {age}-year-old "
                f"{ethnicity} woman with {nationality} heritage."
            ),
            f"Physical Description: {physical}",
            (
                f"Styling: She is styled in {fashion} that reflects her "
                f"{aesthetic.lower()} aesthetic, wearing carefully chosen pieces that complement "
                f"her natural beauty without overwhelming it. The styling is sophisticated yet "
                f"authentic, showcasing her personal aesthetic. {personality}."
            ),
            f"Composition & Pose: {self.COMPOSITION[pose].format(name=name)}",
            f"Lighting: {self.LIGHTING[pose]}",
            f"Technical Specifications: {self.TECHNICAL_SPECS}",
            f"Style & Atmosphere: {self.ATMOSPHERE[pose].format(aesthetic=aesthetic)}",
            f"Critical Requirements: {self.CRITICAL_REQUIREMENTS}",
        ]

        return " ".join(" ".join(s.split()) for s in sections)

    def bulk_prompt(self, persona: Persona, lane: str, index: int = 0) -> str:
        """Generate a rich bulk prompt using natural Z-Image sentence structure.

        Z-Image uses natural sentence structure like camera direction,
        NOT SD-style tag spam. Full sentences with spatial relationships.
        """
        p = persona
        name = p.name
        age = p.age
        ethnicity = p.ethnicity
        city = getattr(p, '_data', {}).get("location", "")
        style_data = getattr(p, '_data', {}).get("style_persona", {})
        aesthetic_str = style_data.get("aesthetic", "contemporary elegance")

        hair_desc = f"{p.hair_color.lower()} {p.hair_length.lower()} {p.hair_texture.lower()} hair"
        eye_desc = f"{p.eye_color.lower()} {p.eye_shape.lower()}-shaped eyes"
        skin_desc = p.skin_tone.lower()

        shot = random.choice(self.SHOT_TYPES)
        lighting = random.choice(self.LIGHTING_KEYWORDS)
        environment = random.choice(self.ENVIRONMENT_MARKERS)

        outfit, action, expression, mood = self._lane_specifics(p, lane, index)

        subs = {
            "shot": shot, "name": name, "age": age, "ethnicity": ethnicity,
            "city": city, "hair_desc": hair_desc, "eye_desc": eye_desc,
            "skin_desc": skin_desc, "aesthetic": aesthetic_str, "outfit": outfit,
            "action": action, "expression": expression, "mood": mood,
            "lighting": lighting, "environment": environment,
            "location": environment,
            "quality": (
                "photorealistic, highly detailed, 8k resolution, professional photography, "
                "sharp focus, natural skin texture with visible pores, realistic lighting, "
                "shot on Sony A7R IV with 85mm lens at f/1.8, shallow depth of field"
            ),
            "camera": (
                "shot on Sony A7R IV, 85mm f/1.8 lens, shallow depth of field, "
                "tack-sharp focus, natural film grain, professional color grading"
            ),
            "photo_style": random.choice([
                "portrait photograph", "editorial photograph",
                "lifestyle photograph", "fashion photograph",
            ]),
            "pose_style": random.choice([
                "confidently", "casually", "elegantly", "playfully",
            ]),
            "bg_style": random.choice([
                "soft bokeh background", "neutral tones", "warm ambient light",
            ]),
            "color_palette": random.choice([
                "warm neutral", "cool pastel", "earth tone", "monochrome",
            ]),
            "color_grading": random.choice([
                "warm film tones", "clean natural colors", "cinematic contrast",
            ]),
            "eye_contact": random.choice([
                "direct eye contact", "looking slightly off-camera",
                "gazing into the distance",
            ]),
            "bg_elements": random.choice([
                "soft greenery", "modern architecture", "warm interior design",
                "city lights in background", "natural outdoor setting",
            ]),
            "outfit_desc": outfit,
            "face_desc": f"Her {eye_desc} and {hair_desc} frame her face beautifully",
        }

        templates = {
            "sfw": self.SFW_TEMPLATES,
            "suggestive": self.SUGGESTIVE_TEMPLATES,
            "spicy": self.SPICY_TEMPLATES,
            "nsfw": self.NSFW_TEMPLATES,
        }

        template_list = templates.get(lane, self.SFW_TEMPLATES)
        template = template_list[index % len(template_list)]

        try:
            prompt = template.format(**subs)
        except KeyError:
            prompt = (
                f"{shot} of {name}, a {age}-year-old {ethnicity} woman with {hair_desc} "
                f"and {eye_desc}. {action} in {environment}. She wears {outfit}. "
                f"Her expression is {expression}. {lighting}. {subs['quality']}."
            )

        return " ".join(prompt.split())

    def negative_prompt(self, lane: str = "sfw") -> str:
        """Z-Image Turbo works best with NO negative prompts."""
        return ""

    # ────────────────────────────────────────────────────────────────
    # Internal helpers
    # ────────────────────────────────────────────────────────────────

    def _lane_specifics(self, p: Persona, lane: str, index: int):
        """Return (outfit, action, expression, mood) for the given lane."""
        wardrobe_data = getattr(p, '_data', {}).get("wardrobe", {})

        sfw_outfits = wardrobe_data.get("casual", []) + wardrobe_data.get("professional", [])
        if not sfw_outfits:
            sfw_outfits = [
                "a fitted blazer over a silk camisole with tailored trousers",
                "a casual oversized sweater with high-waisted jeans",
                "a flowy summer dress in soft pastel tones",
                "athleisure wear with designer sneakers and subtle jewelry",
                "a chic cocktail dress with delicate gold jewelry",
                "a crisp white button-down tucked into wide-leg pants",
                "a knit cardigan over a simple tee with vintage denim",
                "a sleek midi skirt with a tucked-in blouse",
            ]

        suggestive_outfits = wardrobe_data.get("evening", []) + wardrobe_data.get("glamour", [])
        if not suggestive_outfits:
            suggestive_outfits = [
                "a form-fitting evening dress with subtle shimmer",
                "a silk wrap dress that drapes elegantly over her figure",
                "an off-shoulder top paired with a high-waisted skirt",
                "a bodycon dress with tasteful cutouts",
                "lingerie-inspired outerwear layered with a long coat",
                "a satin slip dress with delicate lace trim",
                "a backless halter top with flowing palazzo pants",
            ]

        sfw_actions = [
            "posing confidently with relaxed shoulders",
            "laughing naturally during a candid conversation",
            "walking through the street with purpose and grace",
            "relaxing at a trendy cafe with a warm drink",
            "adjusting her hair casually while looking at the camera",
            "reading a book in beautiful natural light",
            "leaning against a wall with arms crossed casually",
            "looking over her shoulder with a warm smile",
        ]

        suggestive_actions = [
            "posing with alluring confidence and a slight lean",
            "leaning forward subtly with a knowing expression",
            "looking over her shoulder with a captivating smile",
            "reclining on a chaise with elegant poise",
            "stretching languidly in warm morning light",
            "sitting on the edge of a bed with crossed legs",
        ]

        expressions = {
            "sfw": [
                "warm confident smile", "soft genuine laugh", "thoughtful contemplative gaze",
                "playful smirk with raised eyebrow", "serene calm expression",
                "bright engaging smile reaching her eyes",
            ],
            "suggestive": [
                "sultry half-smile", "coy knowing look with lowered lashes",
                "alluring gaze with slightly parted lips", "playful teasing expression",
                "mysterious smile with intense eye contact",
            ],
            "spicy": [
                "intense passionate gaze", "provocative smile with parted lips",
                "seductive expression with bedroom eyes", "bold confident stare",
            ],
            "nsfw": [
                "intimate vulnerable expression", "passionate intensity",
                "uninhibited desire with flushed skin", "breathless anticipation",
            ],
        }

        moods = {
            "sfw": "confident and approachable",
            "suggestive": "flirty and alluring",
            "spicy": "provocative and steamy",
            "nsfw": "intimate and sensual",
        }

        if lane == "sfw":
            outfit = sfw_outfits[index % len(sfw_outfits)]
            action = sfw_actions[index % len(sfw_actions)]
        elif lane == "suggestive":
            outfit = suggestive_outfits[index % len(suggestive_outfits)]
            action = suggestive_actions[index % len(suggestive_actions)]
        elif lane == "spicy":
            outfit = suggestive_outfits[index % len(suggestive_outfits)]
            action = random.choice(suggestive_actions)
        else:
            outfit = random.choice(suggestive_outfits)
            action = random.choice(suggestive_actions)

        expr_list = expressions.get(lane, expressions["sfw"])
        expression = expr_list[index % len(expr_list)]
        mood = moods.get(lane, "confident")

        return outfit, action, expression, mood
