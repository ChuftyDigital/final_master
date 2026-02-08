"""
Cinema-Grade Prompt Engine for Z-Image / Lumina2 Models — Ultimate Edition

Generates ultra-detailed natural language prompts optimized for Z-Image's
Qwen 3.4B semantic understanding.

Reference prompts: 3000-4000+ chars, cinema-grade with per-pose camera specs.
Bulk prompts: 400-800+ chars, two styles (micro-influencer + casual story),
lane-specific building blocks from original template system.

Z-Image reads prompts like camera direction — full sentences with
spatial relationships, not SD-style tag spam.

Based on the original Super Factory premium prompt system with all
techniques from generate_premium_prompts.py, generate_enhanced_flux_workflows.py,
and the Z-Image Master Prompt guide.
"""

import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

from superfactory.models.persona import Persona


class PromptEngine:
    """Generates cinema-grade prompts from persona data.

    Supports two content styles per lane:
    - Micro-Influencer (8K followers): curated, aesthetic, aspirational but authentic
    - Casual Story (300 followers): raw, unfiltered, real moments
    """

    def __init__(self, templates_dir: Optional[str] = None):
        self._templates: Dict[str, Any] = {}
        if templates_dir:
            self._load_templates(templates_dir)

    def _load_templates(self, templates_dir: str):
        """Load lane template JSON files from disk."""
        tdir = Path(templates_dir)
        for lane in ("sfw", "suggestive", "spicy", "nsfw"):
            for name in (f"{lane}.json", f"{lane}_templates.json"):
                path = tdir / name
                if path.exists():
                    with open(path, "r", encoding="utf-8") as f:
                        self._templates[lane] = json.load(f)
                    break

    # ── Hair detail expansions ──────────────────────────────────────

    HAIR_LENGTH_DETAIL = {
        "Long": "cascading down past her shoulders, flowing naturally with subtle movement and catching highlights that reveal dimensional color and healthy shine",
        "Medium": "flowing gracefully around her shoulders with soft natural movement, framing her face with effortless elegance and catching the light beautifully",
        "Short": "styled elegantly and framing her face with modern sophistication, drawing attention to her bone structure and creating a clean, contemporary silhouette",
    }

    EYE_COLOR_DETAIL = {
        "Brown": "deep and expressive with warm undertones that shift between rich chocolate and golden amber in the light, drawing attention with their natural allure",
        "Blue": "vivid and striking with crystalline clarity, shifting between deep sapphire and pale ice depending on the light, immediately captivating",
        "Green": "vibrant and captivating with jewel-like intensity, flecked with subtle gold near the pupil, mesmerizingly beautiful",
        "Hazel": "multifaceted with golden and green flecks that shift mesmerizingly in different lighting, unique and memorable",
        "Amber": "warm and luminous with honey-golden depths that seem to glow from within, rare and striking",
        "Gray": "cool and penetrating with silver undertones and subtle blue-gray depth, enigmatic and elegant",
        "Dark Brown": "intensely dark and expressive with warm mahogany undertones that catch the light beautifully, soulful and captivating",
    }

    SKIN_TONE_DETAIL = {
        "Warm olive": "a warm olive complexion that glows with natural radiance and health, showing beautiful undertones of gold and bronze that catch the light",
        "Porcelain": "porcelain skin with delicate, almost translucent quality, showing natural pink undertones and fine texture with luminous clarity",
        "Caramel": "a rich caramel skin tone that radiates warmth and vitality, with beautiful golden undertones that catch every ray of light",
        "Bronze": "a stunning bronze complexion that catches the light beautifully, with warm copper undertones and healthy luminosity",
        "Fair": "fair, luminous skin with natural warmth, showing subtle rosy undertones and fine, even texture that photographs beautifully",
        "Golden": "golden-toned skin that glows with natural warmth, catching light beautifully with honey undertones and healthy radiance",
        "Deep brown": "rich deep brown skin with beautiful warm undertones, showing extraordinary luminosity and even texture that is stunning on camera",
        "Tan": "sun-kissed tan skin with warm golden undertones, radiating health and natural vitality with beautiful even texture",
        "Ivory": "ivory skin with delicate, refined texture, showing subtle pink warmth and natural luminosity that creates beautiful contrast",
        "Light brown": "light brown skin with warm honey undertones, glowing with natural health and beautiful even texture that catches the light",
    }

    # ── Per-pose camera specifications (from original enhanced generator) ──

    CAMERA_SPECS = {
        "front": (
            "Captured with a Sony A7R IV full-frame mirrorless camera paired with a "
            "Zeiss Batis 85mm f/1.8 lens, the gold standard for portrait photography. "
            "The lens is set to f/2.0 to create a beautifully shallow depth of field that "
            "isolates the subject from the background while maintaining tack-sharp focus on "
            "the eyes. ISO is set to 100 for maximum image quality and dynamic range. "
            "Shutter speed is 1/160s to eliminate any motion blur while maintaining natural "
            "appearance. The image is rendered in photorealistic 8K resolution with exceptional "
            "detail in every element — individual strands of hair, the subtle texture of skin "
            "with visible pores and natural imperfections, fine details in fabric and accessories."
        ),
        "angle": (
            "Captured with a Canon EOS R5 professional camera paired with an exceptional "
            "50mm f/1.2 L lens, renowned for its creamy bokeh and sharp rendering. The aperture "
            "is set to f/1.8 to create a shallow depth of field that isolates her beautifully "
            "while maintaining sharp focus on her near eye. Settings include ISO 200 for clean "
            "images, 1/160s shutter speed for stability, and dual pixel autofocus ensuring "
            "tack-sharp focus on her eyes. The medium format quality of the R5's 45-megapixel "
            "sensor captures extraordinary detail in skin texture, hair strands, and fabric."
        ),
        "natural": (
            "Photographed with a Sony A7R IV camera and a versatile 35mm f/1.4 GM lens that "
            "captures both subject and environment with equal artistry. The wider focal length "
            "allows for environmental storytelling while the fast aperture of f/1.8 creates "
            "beautiful separation between subject and background. Settings include ISO 400 to "
            "handle the natural light conditions, 1/250s shutter speed to freeze the spontaneous "
            "moment, and careful focus on her eyes to maintain sharpness despite the candid "
            "nature of the shot. The 35mm perspective provides a natural field of view that "
            "feels immersive and authentic."
        ),
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

    # ── Post-processing & color grading per pose ────────────────────

    COLOR_GRADING = {
        "front": (
            "The color grading maintains natural skin tones with subtle warmth, professional "
            "contrast that adds depth without looking overprocessed. The background is a smooth, "
            "neutral gradient that provides separation without distraction. Post-processing includes "
            "subtle skin retouching that maintains natural texture while removing temporary blemishes, "
            "color correction for accurate representation, and contrast optimization that enhances "
            "depth. The final image has the quality of a high-end editorial portrait suitable for "
            "magazine covers or luxury brand campaigns."
        ),
        "angle": (
            "The color science prioritizes accurate and flattering skin tones, with the "
            "complexion rendered beautifully through careful white balance and color grading. The "
            "image has a cinematic quality with film-like color response, subtle contrast curves "
            "that add depth, and highlight roll-off that mimics the organic quality of analog "
            "photography. The overall aesthetic evokes high-fashion editorial photography with "
            "the technical precision of modern digital capture."
        ),
        "natural": (
            "The color palette emphasizes the natural warmth of daylight, with skin tones "
            "rendered beautifully through accurate white balance and thoughtful color grading. "
            "The image has an editorial lifestyle photography aesthetic with natural contrast, "
            "organic color response, and a sense of immediacy that connects with viewers. The "
            "background elements, while soft, provide context and environmental storytelling that "
            "adds depth to the portrait."
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

    # ── Bulk generation building blocks (from original Z-Image templates) ──

    SHOT_TYPES = [
        "Close-up portrait", "Medium shot", "Three-quarter view",
        "Environmental portrait", "Candid moment", "Mirror selfie",
        "Front camera view", "Over-the-shoulder", "Profile view", "Full body shot",
    ]

    # Micro-influencer style (curated, aesthetic)
    MI_LIGHTING = [
        "golden hour sunlight streaming through curtains",
        "soft natural daylight from a large window",
        "warm vanity lighting with subtle catchlights in the eyes",
        "ring light with visible catchlights creating even illumination",
        "soft diffused lighting with no harsh shadows",
        "warm tungsten mixed with natural light creating cozy ambiance",
        "clean studio lighting with neutral background",
        "window light with soft directional shadows sculpting her features",
        "backlit with warm rim light separating subject from background",
        "overcast outdoor light for soft even illumination",
    ]

    MI_ENVIRONMENTS = [
        "aesthetically arranged modern apartment with neutral tones and curated decor",
        "trendy cafe with warm ambient lighting and cozy atmosphere",
        "rooftop with city skyline blurred softly in the background",
        "beach at golden hour with soft warm light on skin and sand",
        "luxury hotel room with clean lines and elegant minimal decor",
        "botanical garden with lush greenery creating natural backdrop",
        "urban street with interesting architecture providing depth",
        "cozy reading nook bathed in natural window light",
        "minimalist studio with smooth neutral backdrop and soft shadows",
        "poolside lounge area with tropical atmosphere and warm sunlight",
    ]

    MI_QUALITY = [
        "photorealistic, highly detailed, 8k resolution, professional photography, sharp focus on face, natural skin texture with visible pores, realistic lighting, shot on Sony A7R IV with 85mm lens at f/1.8, shallow depth of field",
        "professional portrait photography, tack-sharp focus, natural film grain, cinematic color grading, warm VSCO aesthetic with slightly lifted blacks, beautiful bokeh",
        "editorial quality photograph, photorealistic skin texture, 8k detail, shot on Canon EOS R5 with 50mm f/1.2 lens, gorgeous shallow depth of field, magazine quality",
        "high-end fashion photography, natural skin with visible pores and fine texture, professional color grading, sharp focus on eyes, subtle background blur",
    ]

    # Casual story style (raw, unfiltered, authentic)
    CS_LIGHTING = [
        "harsh overhead fluorescent creating unflattering shadows",
        "single warm bulb creating a yellow cast on skin",
        "overexposed window light blowing out highlights",
        "blue phone screen glow in a dark room",
        "mixed color temperatures creating uneven illumination",
        "direct flash creating flat harsh light and red-eye",
        "greenish bathroom fluorescents washing out skin tones",
        "dim bedside lamp creating warm but insufficient light",
    ]

    CS_ENVIRONMENTS = [
        "messy bedroom with unmade bed and clothes on the floor",
        "bathroom with slightly dirty mirror and water spots",
        "kitchen with dishes in the sink and cluttered counters",
        "car interior with dashboard visible and unflattering angle",
        "living room couch with blankets and snack wrappers",
        "dorm room with posters on the wall and textbooks scattered",
        "laundry room waiting for dryer with harsh lighting",
        "public bathroom with generic tiles and paper towel dispenser",
    ]

    CS_QUALITY = [
        "front camera selfie quality, slight distortion, grainy, unedited, no filter, raw authentic moment",
        "iPhone front camera, visible grain, slight motion blur, overexposed, completely unfiltered and real",
        "low light phone camera, noisy image, slightly out of focus, harsh shadows, authentic unposed moment",
        "candid phone photo, imperfect framing, natural distortion, raw and unedited with no retouching",
    ]

    # ── Lane-specific building blocks ────────────────────────────────

    # SFW outfits
    SFW_OUTFITS_MI = [
        "a fitted blazer over a silk camisole with tailored trousers and delicate gold jewelry",
        "a casual oversized sweater with high-waisted jeans and clean white sneakers",
        "a flowy summer dress in soft pastel tones with strappy sandals",
        "athleisure wear with designer sneakers and subtle layered necklaces",
        "a chic cocktail dress with delicate gold jewelry and strappy heels",
        "a crisp white button-down tucked into wide-leg pants with a leather belt",
        "a knit cardigan over a simple tee with vintage denim and ankle boots",
        "a sleek midi skirt with a tucked-in blouse and minimalist accessories",
        "matching loungewear set in ribbed neutral tones with fuzzy slippers",
        "a trendy coordinated set with a crop top and high-waisted skirt",
    ]

    SFW_OUTFITS_CS = [
        "an old oversized band t-shirt with visible wear and mismatched pajama shorts",
        "faded hoodie with coffee stains and ratty sweatpants she's had for years",
        "basic white tank top and old underwear, clearly just woke up",
        "oversized college sweater three sizes too big with leggings that have a hole",
        "wrinkled work clothes she hasn't changed out of, looking exhausted",
        "ratty comfortable robe that's seen better days, barely tied",
        "old gym shorts and a sports bra from this morning's workout, still sweaty",
        "mismatched socks, old shorts, and a faded crop top while doing laundry",
    ]

    # SFW actions
    SFW_ACTIONS_MI = [
        "posing confidently with relaxed shoulders and practiced flattering angle",
        "laughing naturally during a candid moment, genuine happiness evident",
        "walking through the street with purpose and grace, hair catching the wind",
        "relaxing at a trendy cafe with a perfectly placed latte art coffee",
        "adjusting her hair casually while looking at the camera with a soft smile",
        "reading a book in beautiful natural light by a window",
        "leaning against a wall with arms crossed casually, looking effortlessly cool",
        "looking over her shoulder with a warm smile that reaches her eyes",
    ]

    SFW_ACTIONS_CS = [
        "lying in bed scrolling her phone with double chin from the angle",
        "sitting on the bathroom floor at 2am looking exhausted",
        "standing in front of her closet in a nothing-to-wear crisis",
        "cooking something questionable in the kitchen with messy hair",
        "studying at her desk surrounded by papers and energy drinks",
        "doing laundry and looking bored out of her mind",
        "eating cereal on the couch at midnight watching trash TV",
        "taking a mirror selfie to send to her friend looking rough",
    ]

    # SFW expressions
    SFW_EXPRESSIONS_MI = [
        "warm confident smile that lights up her entire face",
        "soft genuine laugh with eyes crinkled at the corners",
        "thoughtful contemplative gaze with a hint of mystery",
        "playful smirk with one eyebrow slightly raised",
        "serene calm expression radiating inner peace",
        "bright engaging smile that reaches her eyes, showing genuine warmth",
    ]

    SFW_EXPRESSIONS_CS = [
        "tired blank stare with dark circles visible",
        "grimacing at the camera with self-deprecating humor",
        "mouth slightly open, caught mid-yawn, not camera ready at all",
        "squinting from harsh bathroom light, looking half asleep",
        "confused annoyed expression, clearly not having it today",
        "dead-eyed exhaustion after a long day, zero effort",
    ]

    # Suggestive
    SUGG_OUTFITS = [
        "a lace bodysuit that shows elegant lines while maintaining mystery",
        "a silk slip dress that drapes and catches light on her curves",
        "a sheer robe loosely tied, revealing a hint of what's underneath",
        "an oversized button-down shirt that slides off one shoulder suggestively",
        "a satin camisole with delicate lace trim and matching shorts",
        "a form-fitting evening dress with a thigh-high slit",
        "a backless halter top with flowing palazzo pants that sway as she moves",
        "a bodycon dress with tasteful cutouts that hint at skin beneath",
        "a soft knit sweater dress that clings to her figure, off one shoulder",
        "a strappy bralette visible under an open blazer with nothing else",
    ]

    SUGG_ACTIONS = [
        "leaning back with relaxed confidence and a knowing expression",
        "looking over her shoulder with a captivating, inviting smile",
        "reclining on a chaise with elegant poise and subtle curves on display",
        "stretching languidly in warm morning light, body silhouetted",
        "sitting on the edge of a bed with legs crossed elegantly",
        "standing with hip popped subtly, one hand running through her hair",
        "lying on her side propped on one elbow, gazing at the camera",
        "kneeling with grace on silk sheets, back arched slightly",
    ]

    SUGG_EXPRESSIONS = [
        "soft knowing smile with direct eye contact that suggests invitation",
        "sultry half-smile with lowered lashes and parted lips",
        "alluring gaze with slightly parted lips and bedroom eyes",
        "playful teasing expression with a coy tilt of her head",
        "mysterious smile with intense eye contact that draws you in",
        "vulnerable but confident gaze, relaxed sensuality radiating",
        "quiet confidence with approachable allure and tasteful invitation",
    ]

    SUGG_LIGHTING = [
        "soft romantic candlelight creating warm shadows on skin",
        "warm bedside lamp glow with golden highlights on her curves",
        "window light filtering through sheer curtains creating soft patterns",
        "sunset golden hour streaming through blinds casting warm stripes",
        "softbox creating gentle shadows that sculpt her figure",
        "moody low-key dramatic lighting with rim light defining her silhouette",
    ]

    SUGG_LOCATIONS = [
        "luxury bedroom with soft white linens and warm ambient lighting",
        "hotel room with city view through floor-to-ceiling windows",
        "cozy apartment bedroom with fairy lights and candles",
        "elegant bathroom with marble and soft diffused lighting",
        "sunlit bedroom corner with sheer curtains billowing in breeze",
        "intimate lounge area with velvet furniture and mood lighting",
    ]

    # Spicy
    SPICY_OUTFITS = [
        "a strappy lingerie harness that accentuates her figure",
        "a sheer bodysuit leaving little to the imagination",
        "a wet t-shirt clinging to her body revealing everything underneath",
        "a micro bikini that barely covers, showing maximum skin",
        "a fishnet body stocking with strategic coverage",
        "a latex mini dress that hugs every curve tightly",
        "a barely-there thong and matching bralette in black lace",
        "straps and chains over otherwise bare skin, artistic and provocative",
    ]

    SPICY_ACTIONS = [
        "reclining with full body on display, back arched dramatically",
        "kneeling with inviting posture on silk sheets",
        "lying on stomach looking back seductively over her shoulder",
        "hands exploring her own body with eyes locked on camera",
        "body twisted to accentuate curves, one hand in her hair",
        "seated with legs positioned openly showing confidence",
        "standing with hip thrust forward, body glistening",
        "back turned looking seductively over her shoulder at the camera",
    ]

    SPICY_EXPRESSIONS = [
        "smoldering with desire, eyes half-closed and lips parted",
        "inviting gaze that beckons, completely uninhibited",
        "abandoned to pleasure with flushed skin and heavy breathing",
        "confident sexuality radiating from every pore",
        "intense focus with sultry invitation in her eyes",
        "vulnerable passion mixed with bold confidence",
        "raw sensuality with a hint of playful temptation",
    ]

    SPICY_LIGHTING = [
        "dramatic chiaroscuro shadows defining every curve",
        "warm red mood lighting creating steamy atmosphere",
        "candlelight flickering across glistening skin",
        "spotlight focused on her body, background in darkness",
        "steam-diffused soft light creating ethereal glow",
        "rim light emphasizing her silhouette against dark background",
    ]

    SPICY_LOCATIONS = [
        "steam-filled bathroom with glass shower door",
        "bedroom bathed in warm red ambient light",
        "private jacuzzi with steam rising around her",
        "intimate boudoir with silk and satin everywhere",
        "luxury hotel suite with dramatic city lights behind",
        "canopy bed with silk sheets in warm lamplight",
    ]

    # NSFW
    NSFW_OUTFITS = [
        "completely nude with strategic hand placement",
        "wearing nothing but heels and a necklace",
        "sheer fabric barely covering anything, essentially nude",
        "topless with only a thong, fully confident",
        "naked except for an open robe draped off shoulders",
        "nude with sheets strategically wrapped around her waist",
    ]

    NSFW_ACTIONS = [
        "legs spread wide open exposing everything with confidence",
        "on all fours with back arched, looking back at camera",
        "on her back with legs pulled to her chest, fully exposed",
        "squatting down showing everything, hands on her thighs",
        "lying on her stomach with ass lifted invitingly",
        "sitting on a chair with legs draped over the arms, spread open",
        "standing with one leg raised on furniture, everything visible",
        "kneeling with knees apart, hands running down her body",
        "touching herself intimately while maintaining eye contact",
        "spreading herself open for the camera with both hands",
    ]

    NSFW_EXPRESSIONS = [
        "mouth open in pleasure, moaning with eyes half-closed",
        "biting her lip with intense sexual focus",
        "face flushed with arousal, breathing heavily",
        "uninhibited pleasure written across her entire face",
        "looking desperate with desire, completely lost in the moment",
        "eyes rolled back in ecstasy, skin glistening with sweat",
    ]

    NSFW_LIGHTING = [
        "harsh studio lighting showing every explicit detail clearly",
        "bright spotlights with no shadows hiding anything",
        "warm tungsten glow on sweaty naked skin",
        "ring light creating even illumination on her exposed body",
        "multiple point lighting setup for professional adult photography",
        "high contrast dramatic shadows emphasizing her nude form",
    ]

    NSFW_LOCATIONS = [
        "professional adult photography studio with clean backdrop",
        "luxury penthouse bedroom with mirrors reflecting everything",
        "adult content creator bedroom with professional lighting setup",
        "high-end hotel suite with silk sheets and ambient mood",
        "modern loft with floor-to-ceiling windows and no curtains",
        "private shower with glass walls and steam",
    ]

    # ── Micro-influencer template sentences (per lane) ───────────────

    MI_TEMPLATES = {
        "sfw": [
            "{shot} of a {age}-year-old {ethnicity} woman with {hair_desc} and {eye_desc}, {action} in {location}. She wears {outfit}. Her expression is {expression}. {lighting}. Background shows {environment}. Her {skin_desc} skin glows with natural radiance. {quality}.",
            "{name} posing {pose_style} wearing {outfit}. {location} setting with {bg_style}. {lighting} illuminating her {skin_desc} skin beautifully. She has a {expression}. {camera}. The overall aesthetic is {aesthetic}, curated but authentic.",
            "Professional {photo_style} of {name}, a {age}-year-old {ethnicity} woman from {city}. She is {action}. She wears {outfit}. Her {eye_desc} and {hair_desc} frame her face beautifully. {lighting} creating a {mood} atmosphere. {quality}.",
            "{shot} capturing {name} during {action}. She wears {outfit} in {color_palette} tones. {environment}. {lighting} with {color_grading}. {camera}. Natural skin texture with visible pores, photorealistic detail.",
            "Lifestyle moment of {name} {action} at {location}. She wears {outfit}. {expression} with {eye_contact}. {lighting}. Background features {bg_elements}. {quality}. The image feels candid yet perfectly composed.",
        ],
        "suggestive": [
            "Sensual portrait of {name}, a {age}-year-old {ethnicity} woman, {action} in {location}. She wears {outfit} that {reveals}. {expression}. {lighting} caresses her {skin_desc} skin creating warm highlights. {quality}.",
            "Alluring {shot} of {name} during {action}. She wears {outfit}. Her {skin_desc} skin catches the {lighting} beautifully. {expression}. The mood is {mood} and inviting. {camera}.",
            "Tasteful boudoir photograph of {name} in {location}, wearing {outfit}. {action}. {lighting} bathes her figure in warm golden light. {expression}. {quality}. Elegant sensuality, not explicit.",
            "{name} captured in a moment of quiet confidence, wearing {outfit} in {location}. {action}. {lighting} creates {shadows} highlighting her silhouette. {expression}. Sophisticated sensuality with professional boudoir quality.",
            "Glamorous {photo_style} of {name} in {outfit}. {action} with {mood} energy in {location}. Her {hair_desc} falls naturally as {lighting} illuminates her {eye_desc}. {quality}.",
        ],
        "spicy": [
            "Provocative {shot} of {name}, a {age}-year-old {ethnicity} woman, {action} in {location}. She wears {outfit}. {expression}. {lighting} accentuating every curve of her {skin_desc} body. {quality}.",
            "Steamy {photo_style} of {name} in {outfit}. {action}. {lighting} creates {shadows} on her glistening {skin_desc} skin. {expression}. Her body is on full display. {camera}.",
            "Provocative scene: {name} in {location}, wearing {outfit}. {action}. {expression}. {lighting} defines her body contours dramatically. Erotic art photography with sophisticated composition. {quality}.",
            "Intense {shot} of {name} wearing {outfit} in {location}. {action}. {lighting} bathes the scene in {glow}. {expression}. Her {hair_desc} is tousled and wild. Provocative fine art quality.",
        ],
        "nsfw": [
            "Explicit {shot} of {name}, a {age}-year-old {ethnicity} woman, {action} in {location}. She is {outfit}. Her body is fully exposed and {arousal_state}. {expression}. {lighting} illuminates every intimate detail. {quality}.",
            "Hardcore adult scene: {name} {action}, {outfit}. Her {body_desc} is {arousal_state}. {expression}. {location}. {lighting} on her {skin_desc} skin. Professional adult photography quality.",
            "Explicit content: {name} in {location}, {action}. {outfit}. {expression}. {lighting} shows {detail}. Her body {arousal_state}. Premium adult content photography, uncensored.",
            "Adult entertainment: {name} {action} in {location}. {outfit}. {expression}. {lighting} creating {shadows} on {skin_desc} flesh. {quality}. Uninhibited, graphic, professional production quality.",
        ],
    }

    # Casual story template sentences (per lane)
    CS_TEMPLATES = {
        "sfw": [
            "Candid {shot} of {name}, a {age}-year-old {ethnicity} woman with {features}, currently {state}. {hair_state}. She wears {outfit}. {expression}. {lighting}. Background shows {environment}. {quality}.",
            "Real moment: {name} {action}. {appearance}. She wears {outfit}. {expression}. {lighting} from {light_source}. {environment}. Unfiltered, authentic, no editing.",
            "Unfiltered {shot} of {name}. {hair_state}. {outfit}. {action}. {expression}. {lighting}. {environment}. {quality}. This is the real her, no pretenses.",
            "{name} captured in an authentic moment, {action}. {outfit}. {expression}. {lighting}. Her {skin_desc} skin shows real texture with natural imperfections. {environment}. {quality}.",
        ],
        "suggestive": [
            "Candid intimate {shot} of {name}, caught in an unintentional moment of {vulnerability}. {appearance} adds to authentic allure. She wears {outfit}. {expression}. {lighting}. {environment}. Raw, unposed intimacy.",
            "Real moment: {name} {action} in {location}. {outfit} suggests relaxed intimacy. {expression}. Morning light through window. Bedhead hair and no makeup. Candid vulnerability.",
            "Behind the scenes: {name} during a personal moment, {action}. {outfit}. {expression}. {lighting}. Lived-in space with personal items. Unpolished, genuine allure.",
        ],
        "spicy": [
            "Candid {shot}: {name} caught in a private moment of self-exploration. Natural state without performance. {lighting}. Messy bedroom background. Authentic vulnerability.",
            "Real intimacy: {name} {action} in her personal space. Unposed position showing natural form. {lighting} creating real shadows. Genuine expression, not performed. Raw eroticism.",
            "Unfiltered moment: {name} during a private activity. Comfortable with her body rather than posing. Natural curves in relaxed position. {lighting}. Authentic sexuality.",
        ],
        "nsfw": [
            "Candid explicit moment: {name} {action} alone in her bedroom. Real body with natural imperfections. Casual setting, not a studio. {lighting}. Private moment captured without judgment. Raw, unfiltered adult content.",
            "Behind closed doors: {name} in personal intimacy, {action}. Real body, natural imperfections visible. {lighting}. Authentic bedroom setting. Genuine pleasure, not performed.",
            "Unfiltered explicit: {name} {action}. No professional lighting or staging. Real room, real body, real pleasure. Phone camera quality. Completely raw and authentic.",
        ],
    }

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
        e_detail = self.EYE_COLOR_DETAIL.get(e_color, "striking and expressive with natural depth and allure")
        parts.append(
            f"Her eyes are {e_color.lower()} and {e_shape.lower()}-shaped, {e_detail}"
        )

        skin = p.skin_tone
        skin_detail = self.SKIN_TONE_DETAIL.get(
            skin, f"beautiful {skin.lower()} skin with natural radiance and healthy luminosity"
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

        Uses per-pose camera specs from the original enhanced workflow generator.
        """
        p = persona
        name = p.name
        age = p.age
        ethnicity = p.ethnicity
        nationality = p.nationality
        style_persona = getattr(p, '_data', {}).get("style_persona", {})
        aesthetic = style_persona.get("aesthetic", "sophisticated elegance")
        fashion = style_persona.get("fashion_sense", "elegant contemporary style")
        niche = getattr(p, '_data', {}).get("niche", "")
        personality = ""
        if p.personality_summary:
            personality = p.personality_summary.split(".")[0]

        physical = self._physical_description(p)

        sections = [
            (
                f"Professional portrait photograph of {name}, a {age}-year-old "
                f"{ethnicity} woman with {nationality} heritage. This is a close-up "
                f"head-and-shoulders portrait of a real person, not a product shot or flat-lay."
            ),
            f"Composition & Pose: {self.COMPOSITION[pose].format(name=name)}",
            f"Physical Description: {physical}",
            (
                f"Styling: She is styled in {fashion} that reflects her "
                f"{niche.lower() + ' ' if niche else ''}{aesthetic.lower()} aesthetic, "
                f"wearing carefully chosen pieces that complement her natural beauty without "
                f"overwhelming it. {personality}."
            ),
            f"Lighting: {self.LIGHTING[pose]}",
            f"Technical Specifications: {self.CAMERA_SPECS[pose]}",
            f"{self.COLOR_GRADING[pose]}",
            f"Style & Atmosphere: {self.ATMOSPHERE[pose].format(aesthetic=aesthetic)}",
            f"Critical Requirements: {self.CRITICAL_REQUIREMENTS}",
        ]

        return " ".join(" ".join(s.split()) for s in sections)

    def bulk_prompt(self, persona: Persona, lane: str, index: int = 0) -> str:
        """Generate a rich bulk prompt using Z-Image natural sentence structure.

        Alternates between micro-influencer style (even indices) and
        casual story style (odd indices) for visual variety.
        """
        # Alternate between micro-influencer and casual story styles
        is_micro = (index % 2 == 0)

        if is_micro:
            return self._bulk_micro_influencer(persona, lane, index)
        else:
            return self._bulk_casual_story(persona, lane, index)

    def negative_prompt(self, lane: str = "sfw") -> str:
        """FLUX benefits from negative prompts for quality control."""
        return (
            "blurry, low quality, cartoon, anime, distorted face, bad anatomy, "
            "deformed features, unnatural skin, plastic look, oversaturated, "
            "jpeg artifacts, watermark, text, logo"
        )

    # ────────────────────────────────────────────────────────────────
    # Internal: Micro-Influencer bulk prompts
    # ────────────────────────────────────────────────────────────────

    def _bulk_micro_influencer(self, persona: Persona, lane: str, index: int) -> str:
        """Generate a curated, aesthetic micro-influencer style prompt."""
        p = persona
        subs = self._build_substitutions(p, lane, index, style="mi")

        templates = self.MI_TEMPLATES.get(lane, self.MI_TEMPLATES["sfw"])
        template = templates[index % len(templates)]

        try:
            prompt = template.format(**subs)
        except KeyError:
            prompt = self._fallback_prompt(subs, lane)

        return " ".join(prompt.split())

    # ────────────────────────────────────────────────────────────────
    # Internal: Casual Story bulk prompts
    # ────────────────────────────────────────────────────────────────

    def _bulk_casual_story(self, persona: Persona, lane: str, index: int) -> str:
        """Generate a raw, unfiltered casual story style prompt."""
        p = persona
        subs = self._build_substitutions(p, lane, index, style="cs")

        templates = self.CS_TEMPLATES.get(lane, self.CS_TEMPLATES["sfw"])
        template = templates[index % len(templates)]

        try:
            prompt = template.format(**subs)
        except KeyError:
            prompt = self._fallback_prompt(subs, lane)

        return " ".join(prompt.split())

    # ────────────────────────────────────────────────────────────────
    # Substitution builder
    # ────────────────────────────────────────────────────────────────

    def _build_substitutions(self, p: Persona, lane: str, index: int, style: str = "mi") -> dict:
        """Build the full substitution dictionary for template filling."""
        name = p.name
        age = p.age
        ethnicity = p.ethnicity
        city = getattr(p, '_data', {}).get("location", "")
        style_data = getattr(p, '_data', {}).get("style_persona", {})
        aesthetic = style_data.get("aesthetic", "contemporary elegance")

        hair_desc = f"{p.hair_color.lower()} {p.hair_length.lower()} {p.hair_texture.lower()} hair"
        eye_desc = f"{p.eye_color.lower()} {p.eye_shape.lower()}-shaped eyes"
        skin_desc = p.skin_tone.lower()

        # Lane-specific selections
        outfit, action, expression = self._lane_content(p, lane, index, style)

        # Style-specific selections
        if style == "mi":
            lighting = random.choice(self.MI_LIGHTING)
            environment = random.choice(self.MI_ENVIRONMENTS)
            quality = random.choice(self.MI_QUALITY)
        else:
            lighting = random.choice(self.CS_LIGHTING)
            environment = random.choice(self.CS_ENVIRONMENTS)
            quality = random.choice(self.CS_QUALITY)

        # Lane-specific location/lighting overrides
        location = environment
        if lane == "suggestive":
            location = random.choice(self.SUGG_LOCATIONS) if style == "mi" else environment
            if style == "mi":
                lighting = random.choice(self.SUGG_LIGHTING)
        elif lane == "spicy":
            location = random.choice(self.SPICY_LOCATIONS) if style == "mi" else environment
            if style == "mi":
                lighting = random.choice(self.SPICY_LIGHTING)
        elif lane == "nsfw":
            location = random.choice(self.NSFW_LOCATIONS) if style == "mi" else environment
            if style == "mi":
                lighting = random.choice(self.NSFW_LIGHTING)

        return {
            "shot": random.choice(self.SHOT_TYPES),
            "name": name, "age": age, "ethnicity": ethnicity,
            "city": city, "hair_desc": hair_desc, "eye_desc": eye_desc,
            "skin_desc": skin_desc, "aesthetic": aesthetic,
            "outfit": outfit, "action": action, "expression": expression,
            "lighting": lighting, "environment": environment, "location": location,
            "quality": quality,
            "mood": self._lane_mood(lane),
            "features": f"{hair_desc} and {eye_desc}",
            "camera": "shot on Sony A7R IV, 85mm f/1.8, shallow depth of field, tack-sharp focus, natural film grain, professional color grading",
            "photo_style": random.choice(["portrait photograph", "editorial photograph", "lifestyle photograph", "fashion photograph"]),
            "pose_style": random.choice(["confidently", "casually", "elegantly", "playfully"]),
            "bg_style": random.choice(["soft bokeh background", "neutral tones", "warm ambient light"]),
            "bg_elements": random.choice(["soft greenery", "modern architecture", "warm interior design", "city lights in background", "natural outdoor setting"]),
            "color_palette": random.choice(["warm neutral", "cool pastel", "earth tone", "monochrome"]),
            "color_grading": random.choice(["warm film tones", "clean natural colors", "cinematic contrast"]),
            "eye_contact": random.choice(["direct eye contact", "looking slightly off-camera", "gazing into the distance"]),
            "reveals": random.choice(["hints at curves beneath", "drapes elegantly over her figure", "accentuates her silhouette"]),
            "shadows": random.choice(["dramatic shadows", "gentle shadows", "warm shadows"]),
            "glow": random.choice(["warm golden glow", "intimate red-tinted light", "soft amber warmth"]),
            "vulnerability": random.choice(["natural beauty", "authentic allure", "unposed intimacy"]),
            "appearance": f"Her {hair_desc} is messy and natural, {skin_desc} skin showing real texture",
            "state": random.choice(["looking tired but naturally beautiful", "just woke up", "lounging after a long day", "getting ready for bed"]),
            "hair_state": random.choice([f"Her {p.hair_color.lower()} hair is messy and unbrushed", f"Hair in a falling-apart bun with flyaways", f"Bedhead {p.hair_color.lower()} hair, hasn't looked in a mirror"]),
            "light_source": random.choice(["harsh bathroom light", "phone screen", "bedside lamp", "kitchen overhead light"]),
            "body_desc": f"{skin_desc} body with natural curves",
            "arousal_state": random.choice(["glistening with arousal", "flushed and responsive", "visibly excited", "dripping wet"]),
            "detail": random.choice(["every intimate detail", "full nudity in sharp focus", "explicit anatomy clearly visible"]),
        }

    def _lane_content(self, p: Persona, lane: str, index: int, style: str):
        """Get (outfit, action, expression) based on lane and style."""
        # Get persona wardrobe
        wardrobe_raw = getattr(p, '_data', {}).get("wardrobe", [])
        persona_outfits = wardrobe_raw if isinstance(wardrobe_raw, list) else []

        if lane == "sfw":
            if style == "mi":
                outfits = persona_outfits if persona_outfits else self.SFW_OUTFITS_MI
                actions = self.SFW_ACTIONS_MI
                expressions = self.SFW_EXPRESSIONS_MI
            else:
                outfits = self.SFW_OUTFITS_CS
                actions = self.SFW_ACTIONS_CS
                expressions = self.SFW_EXPRESSIONS_CS
        elif lane == "suggestive":
            outfits = self.SUGG_OUTFITS
            actions = self.SUGG_ACTIONS
            expressions = self.SUGG_EXPRESSIONS
        elif lane == "spicy":
            outfits = self.SPICY_OUTFITS
            actions = self.SPICY_ACTIONS
            expressions = self.SPICY_EXPRESSIONS
        elif lane == "nsfw":
            outfits = self.NSFW_OUTFITS
            actions = self.NSFW_ACTIONS
            expressions = self.NSFW_EXPRESSIONS
        else:
            outfits = self.SFW_OUTFITS_MI
            actions = self.SFW_ACTIONS_MI
            expressions = self.SFW_EXPRESSIONS_MI

        outfit = outfits[index % len(outfits)]
        action = actions[index % len(actions)]
        expression = expressions[index % len(expressions)]

        return outfit, action, expression

    def _lane_mood(self, lane: str) -> str:
        """Get the mood descriptor for a lane."""
        return {
            "sfw": "confident and approachable",
            "suggestive": "flirty and alluring",
            "spicy": "provocative and steamy",
            "nsfw": "explicit and uninhibited",
        }.get(lane, "confident")

    def _fallback_prompt(self, subs: dict, lane: str) -> str:
        """Generate a reliable fallback prompt if template filling fails."""
        return (
            f"{subs['shot']} of {subs['name']}, a {subs['age']}-year-old {subs['ethnicity']} "
            f"woman with {subs['hair_desc']} and {subs['eye_desc']}. {subs['action']} in "
            f"{subs['location']}. She wears {subs['outfit']}. Her expression is "
            f"{subs['expression']}. {subs['lighting']}. {subs['quality']}."
        )
