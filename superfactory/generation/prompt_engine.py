"""
Cinema-Grade Prompt Engine for FLUX.1 Dev — Ultimate Edition

Generates ultra-detailed natural language prompts optimized for FLUX's
superior prompt adherence and photorealistic output.

Reference prompts: 3000-4500+ chars, editorial fashion photography quality
with golden hour lighting, natural environments, and raw skin authenticity.
Bulk prompts: 400-800+ chars, two styles (micro-influencer + casual story),
lane-specific building blocks from original template system.

FLUX excels with detailed natural language descriptions — full sentences with
spatial relationships, lighting direction, and specific photographic technique.

Based on the original Super Factory premium prompt system with all
techniques from generate_premium_prompts.py and generate_enhanced_flux_workflows.py.
Target quality: Vogue/Elle editorial fashion photography shot on location.
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
        "Long": "cascading down past her shoulders, windblown and naturally tousled with individual strands catching the golden light, baby hairs at the hairline visible, with dimensional color and healthy movement",
        "Medium": "flowing around her shoulders with natural windblown movement, loose strands framing her face with effortless beauty, catching golden highlights and moving with the breeze",
        "Short": "styled with natural texture and slight windblown movement, drawing attention to her bone structure with a contemporary silhouette, fine baby hairs visible at the hairline",
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
        "Warm olive": "a warm olive complexion with visible pores and natural texture, scattered light freckles across the nose and cheeks from sun exposure, beautiful undertones of gold and bronze that glow in natural light, with the real lived-in quality of skin that has seen sunshine",
        "Porcelain": "porcelain skin with delicate translucent quality, showing natural pink undertones, visible fine veins at the temples, scattered freckles and sun marks, and the beautiful imperfect texture of real skin with fine peach fuzz catching the light",
        "Caramel": "a rich caramel skin tone with beautiful natural texture showing visible pores and subtle tonal variations, warm golden undertones that catch every ray of golden hour light, with the authentic luminosity of real sun-kissed skin",
        "Bronze": "a stunning bronze complexion with rich natural texture, visible pores and subtle sun marks, warm copper undertones creating depth, and the healthy authentic glow of real skin that has been kissed by sunlight",
        "Fair": "fair luminous skin with natural warmth, visible freckles scattered across the nose and cheeks, subtle rosy undertones, fine peach fuzz along the jawline catching the light, and the authentic delicate texture of real skin",
        "Golden": "golden-toned skin with natural texture and visible pores, honey undertones that glow magnificently in warm light, subtle sun freckles and the authentic radiant quality of real skin illuminated by golden hour",
        "Deep brown": "rich deep brown skin with extraordinary natural luminosity, visible fine texture and pores, warm undertones that catch and reflect golden light beautifully, with the stunning authentic quality of real skin in natural sunlight",
        "Tan": "sun-kissed tan skin with visible freckles and sun marks from real outdoor living, warm golden undertones, natural texture with visible pores, and the authentic healthy glow of skin that knows sunshine",
        "Ivory": "ivory skin with delicate visible texture, scattered natural freckles, subtle pink warmth with fine veins visible at the temples, and the beautiful raw quality of real fair skin in warm natural light",
        "Light brown": "light brown skin with warm honey undertones, natural texture with visible pores and subtle tonal variations, the authentic glow of real skin catching golden hour light beautifully",
    }

    # ── Camera + post-processing (same for all reference poses for consistency) ──

    REFERENCE_TECHNICAL_SPECS = (
        "Captured with professional-grade equipment using a Sony A7R IV full-frame "
        "mirrorless camera paired with a Zeiss Batis 85mm f/1.8 lens, the gold standard "
        "for portrait photography. The lens is set to f/2.0 to create a beautifully shallow "
        "depth of field with gorgeous creamy bokeh in the background while maintaining "
        "tack-sharp focus on the eyes. ISO is set to 200 for maximum image quality in "
        "natural light conditions. Shutter speed is 1/250s to freeze windblown hair and "
        "natural movement. The image is rendered in photorealistic 8K resolution with "
        "exceptional detail in every element — individual windblown strands of hair catching "
        "golden light, the rich texture of real skin with visible pores, natural freckles, "
        "fine lines, sun marks, and authentic imperfections that tell the story of a real "
        "person. The color grading is warm and golden with rich amber tones, emphasizing "
        "the golden hour warmth on skin while maintaining accurate but sun-kissed skin "
        "tones. No skin retouching — all natural texture, blemishes, and imperfections "
        "are preserved. The final image has the quality of a high-end editorial fashion "
        "photograph shot on location for Vogue or Sports Illustrated, with the raw "
        "authenticity and warmth of natural golden hour light."
    )

    # Keep per-pose camera specs for BULK generation variety
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
            "Stunning golden hour sunlight approximately 20 minutes before sunset, with the "
            "warm low-angle sun creating gorgeous directional light that wraps around her face and "
            "body. The golden light paints her skin with warm amber and honey tones, emphasizing "
            "every natural texture — freckles, pores, and fine peach fuzz catching the light. The "
            "warm color temperature of approximately 3200K-3800K creates that coveted golden hour "
            "glow on skin. Natural environmental light with no artificial fill — shadows are soft "
            "and warm, not harsh. The sun creates natural catchlights in the eyes and a warm "
            "luminosity across the skin that cannot be replicated in a studio."
        ),
        "angle": (
            "Dramatic golden hour backlighting with the low sun positioned behind and to the "
            "side of the subject, creating a stunning warm rim light that outlines her hair and "
            "silhouette with a glowing golden halo. Individual strands of windblown hair are "
            "illuminated and backlit like golden threads. The backlighting creates beautiful lens "
            "flare and warm atmospheric haze. Her face is lit by the soft warm bounce light from "
            "the surrounding environment — sand, water, or warm surfaces reflecting golden light "
            "back as natural fill. This creates dimensional sculpting of her facial features with "
            "warm shadows and luminous highlights."
        ),
        "natural": (
            "Late golden hour sunlight creating a warm, glowing atmosphere with the sun very low "
            "on the horizon. The light is soft, directional, and deeply warm, casting long gentle "
            "shadows and bathing everything in rich amber and golden tones. A natural warm breeze "
            "adds movement to hair and any loose fabric. The environmental light wraps around the "
            "subject with beautiful warmth, creating the intimate feeling of a perfect sunset "
            "moment. The quality of light is ephemeral and magical — the kind of natural illumination "
            "that makes everything look beautiful and alive. No artificial lighting whatsoever, "
            "pure natural golden hour magic."
        ),
    }

    # ── Composition per pose (from original premium generator) ──────

    COMPOSITION = {
        "front": (
            "Head-and-shoulders portrait with {name} facing the camera in a natural outdoor "
            "setting. The composition follows the rule of thirds with eyes positioned along the "
            "upper horizontal third line. The frame captures from mid-chest upward with the "
            "natural environment softly blurred behind her. Her hair has natural movement from "
            "a gentle breeze, with loose strands catching the golden light. Expression is warm "
            "and direct — a natural, unforced look with slightly parted lips and intense eye "
            "contact that draws the viewer in. Skin shows natural texture with visible pores, "
            "light freckles or sun marks, and authentic warmth from the golden light. This is "
            "an editorial fashion portrait, not a studio headshot — it feels alive and present."
        ),
        "angle": (
            "Dynamic three-quarter view with {name}'s body angled away from the camera "
            "while her head turns back toward the lens with intense eye contact. The composition "
            "emphasizes her cheekbones and jawline through the angular perspective with dramatic "
            "golden hour backlighting creating a glowing rim light around her hair and shoulders. "
            "Windblown hair adds energy and movement to the frame, with individual strands backlit "
            "like golden threads. Shoulders are relaxed and natural, not posed stiffly. Her "
            "expression is captivating — a slight knowing smile with eyes that communicate "
            "confidence and personality. Visible skin texture with natural warmth from the "
            "golden light. The background shows a soft, dreamy outdoor environment."
        ),
        "natural": (
            "Candid editorial portrait capturing {name} in a genuine, relaxed moment outdoors. "
            "The pose is organic and spontaneous — perhaps running a hand through her windblown "
            "hair, or caught mid-laugh with authentic joy. The frame is slightly wider, showing "
            "more of the natural environment and body language. Her hair is tousled naturally by "
            "the wind, messy in a beautiful way. Expression radiates genuine warmth and personality "
            "— this is the real her, unguarded and naturally beautiful. Skin glows with golden hour "
            "warmth, showing every natural freckle and texture. The composition feels like a "
            "perfect candid moment captured by a fashion photographer — spontaneous yet stunning, "
            "the kind of shot that becomes a magazine cover."
        ),
    }

    # ── Style / atmosphere per pose ─────────────────────────────────

    ATMOSPHERE = {
        "front": (
            "The image embodies {aesthetic} with the raw, editorial quality of a Vogue or "
            "Elle fashion spread shot on location during golden hour. The overall mood is warm, "
            "confident, and magnetically present — she owns the moment completely. The aesthetic "
            "is natural luxury — no artificial studio perfection, but the effortless beauty of a "
            "real woman in beautiful natural light. The golden hour warmth suffuses the entire image "
            "with amber and honey tones. This is the definitive reference image — capturing her "
            "essence with the authenticity and warmth that makes a viewer feel connected."
        ),
        "angle": (
            "Capturing {aesthetic} with the dramatic, cinematic quality of a high-fashion "
            "editorial shot at magic hour. The mood is captivating and dynamic, with the backlit "
            "golden light creating a dreamlike atmosphere. The aesthetic feels like the best frame "
            "from a fashion film — alive with movement, warmth, and personality. The dramatic "
            "rim lighting and windblown hair create visual poetry. This angle provides crucial "
            "three-dimensional reference while showing her personality and natural charisma."
        ),
        "natural": (
            "Authentic {aesthetic} with the intimate, warm quality of a moment captured between "
            "posed shots — the genuine, unguarded beauty that fashion photographers live for. "
            "The mood is warm, genuine, and irresistibly human. The aesthetic is raw editorial "
            "beauty — imperfect in the most beautiful way, like a candid frame that becomes the "
            "magazine's hero image. Golden light, natural wind, authentic expression — everything "
            "combines to create an image that feels effortlessly beautiful and deeply personal."
        ),
    }

    # ── Post-processing & color grading per pose ────────────────────

    COLOR_GRADING = {
        "front": (
            "The color grading leans into the golden hour warmth with rich amber and honey "
            "tones painting the skin, while maintaining enough accuracy that her natural "
            "complexion reads true. Shadows are warm, not cool — filled with reflected golden "
            "light from the environment. The background is a natural outdoor setting rendered in "
            "soft bokeh with warm golden tones. Zero skin retouching — natural pores, freckles, "
            "fine lines, and sun marks are all visible and beautiful. The final image has the "
            "warm, lived-in quality of the best editorial fashion photography — real, raw, and "
            "stunning."
        ),
        "angle": (
            "The color science embraces the dramatic warmth of backlit golden hour, with skin "
            "tones glowing with amber and gold undertones. The rim light creates warm highlight "
            "edges while shadows remain soft and golden. The image has a cinematic quality with "
            "film-like color response reminiscent of Kodak Portra 400 — organic highlight roll-off, "
            "warm midtones, and rich but not crushed shadows. Lens flare and atmospheric haze "
            "add to the dreamy, warm editorial quality."
        ),
        "natural": (
            "The color palette fully embraces the ephemeral golden hour warmth, with the entire "
            "image bathed in rich sunset tones. Skin practically glows with golden warmth, and "
            "the environmental background contributes warm, soft colors that complement her "
            "complexion. The look is that of high-end fashion editorial shot on location at the "
            "perfect moment — warm, organic color response with natural contrast and the beautiful "
            "imperfection of real light. The background elements provide environmental context and "
            "storytelling that grounds the image in reality."
        ),
    }

    CRITICAL_REQUIREMENTS = (
        "This image MUST show hyper-photorealistic quality indistinguishable from a real "
        "photograph. The skin must show REAL texture — visible pores, natural freckles, fine "
        "peach fuzz on the face catching the golden light, subtle sun damage or age marks, "
        "tiny imperfections and beauty marks that make a real face look REAL. Absolutely NO "
        "artificial smoothness, NO airbrushed skin, NO plastic appearance. Hair must appear as "
        "individual strands with natural flyaways, baby hairs at the hairline, and wind-tousled "
        "movement — not perfectly styled. Eyes must have realistic catchlights reflecting the "
        "natural environment and deep, soulful dimension. Skin must show the golden warmth of "
        "real sunlight with subsurface scattering visible on thinner skin like ears and nose. "
        "The image should look like it was captured by a world-class fashion photographer like "
        "Peter Lindbergh or Mario Testino — raw, authentic beauty elevated by extraordinary "
        "light and composition. Facial features must be consistent, distinctive, and deeply "
        "human. This is a REAL woman, not a digital creation."
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
                f"Subject: Editorial fashion photograph of {name}, a {age}-year-old "
                f"{ethnicity} woman with {nationality} heritage, shot on location during "
                f"golden hour with natural wind and warm sunlight."
            ),
            f"Physical Description: {physical}",
            f"Composition & Pose: Composition: {self.COMPOSITION[pose].format(name=name)}",
            f"Lighting: {self.LIGHTING[pose]}",
            f"Technical Specifications: {self.REFERENCE_TECHNICAL_SPECS}",
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
            "deformed features, plastic skin, airbrushed skin, overly smooth skin, "
            "artificially perfect skin, studio backdrop, grey background, white background, "
            "neutral background, studio lighting, ring light, softbox, "
            "oversaturated, jpeg artifacts, watermark, text, logo, "
            "doll-like, mannequin, wax figure, CGI, 3D render"
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
