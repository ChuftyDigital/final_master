#!/usr/bin/env python3
"""
Generated Content for AI Influencer Prompt Engine v3.0
=======================================================
Contains niche-specific scenarios and outfit sets for all 21 character niches.

GENERATED_NICHE_SCENARIOS: 19 niches x 4 lanes x 8 scenarios each
GENERATED_OUTFIT_SETS: 3 lanes (suggestive, spicy, nsfw) x 21 niches x 4 outfits each

These are designed to be merged into the main prompt_engine.py dictionaries.
"""

# ---------------------------------------------------------------------------
# NICHE SCENARIOS - 19 niches that currently fall back to "default"
# Each niche has 4 lanes (sfw, suggestive, spicy, nsfw) with 8 scenarios each.
# Scenarios describe SCENE/SETTING/MOOD only - outfits are handled separately.
# ---------------------------------------------------------------------------
GENERATED_NICHE_SCENARIOS = {

    "Luxury Travel/Aviation": {
        "sfw": [
            "stepping off a private jet onto a sunlit tarmac, her silhouette framed against the gleaming fuselage and endless blue sky",
            "seated in a first-class cabin with champagne in hand, city lights twinkling through the oval window at thirty thousand feet",
            "walking through the grand marble lobby of a five-star hotel in Dubai, golden light reflecting off polished floors",
            "leaning on the railing of a private balcony in Santorini, whitewashed buildings and the Aegean Sea stretching behind her",
            "browsing a luxury boutique in the Milan Galleria, arched glass ceilings soaring overhead, shopping bags in hand",
            "sipping espresso at a sidewalk cafe in Paris, the Eiffel Tower soft-focused in the background, effortlessly chic",
            "standing at the bow of a luxury yacht anchored in the Amalfi Coast, wind in her hair, coastline glowing at sunset",
            "checking in at an exclusive airport lounge, passport and boarding pass in hand, poised and worldly"
        ],
        "suggestive": [
            "reclining in a first-class lie-flat seat with a silk sleep mask pushed up on her forehead, blouse slightly loosened after a long flight",
            "stepping out of an infinity pool at a Maldives overwater villa, water streaming down her sun-warmed skin, ocean stretching to the horizon",
            "lounging on a private terrace in Monaco, legs crossed on the daybed, the harbor full of yachts glittering below",
            "posing in the doorway of a luxury hotel suite, the plush king bed visible behind her, city skyline through floor-to-ceiling windows",
            "leaning against the polished mahogany bar of a rooftop lounge in Tokyo, city lights reflected in the glass behind her",
            "sitting on the edge of a rooftop hot tub in Bali, steam curling around her shoulders, jungle canopy below",
            "walking barefoot through the shallow surf of a private island beach, wet sand catching golden light under her feet",
            "draped across a velvet chaise in a boutique hotel lobby, one heel dangling from her toe, champagne flute balanced lazily"
        ],
        "spicy": [
            "in a penthouse suite overlooking the Singapore skyline, perched on the window ledge in intimate attire, city lights painting her skin",
            "in a marble bathroom of a Parisian hotel, candlelight flickering across the freestanding copper tub and her bare shoulders",
            "on silk sheets in a Moroccan riad, warm lamplight filtering through carved screens, the air heavy with jasmine",
            "in the master cabin of a superyacht at anchor, moonlight streaming through the porthole onto rumpled linen",
            "standing before a floor-to-ceiling mirror in a Milan hotel suite, soft golden light tracing her silhouette",
            "reclining on a daybed in a private cabana in Ibiza, sheer curtains billowing, the bass of distant music felt more than heard",
            "in a Japanese onsen-style private bath, steam rising around her, lantern light warm on wet skin",
            "on the terrace of a cliffside villa in Positano, moonlight on the Mediterranean, wrapped in nothing but the warm night air"
        ],
        "nsfw": [
            "an artistic nude on white linen sheets in a Santorini suite, morning light flooding through the open terrace doors",
            "standing nude at the panoramic window of a high-rise hotel, the city sprawled below, her reflection ghosting in the glass",
            "in a deep soaking tub in a Japanese ryokan, water at her waist, paper lanterns casting amber warmth on bare skin",
            "reclining on the sundeck of a private yacht at dawn, completely bare, the sea breeze and first light the only things touching her",
            "a figure study on the private beach of a Maldives villa, warm sand beneath her, turquoise water lapping at the shore",
            "in a luxury rain shower with floor-to-ceiling glass overlooking the ocean, water cascading over every curve",
            "draped across a chaise on a moonlit balcony in Amalfi, nude and unhurried, the warm Mediterranean night embracing her",
            "in the candlelit master suite of a French chateau, bare on antique silk, firelight dancing across her body"
        ]
    },

    "Gaming/E-Sports (Cute/Casual)": {
        "sfw": [
            "sitting cross-legged in a neon-lit gaming chair, RGB lights casting purple and blue hues, multiple monitors glowing with game lobbies",
            "at a gaming convention posing beside a massive character statue, lanyard badges around her neck, excited crowd blurred behind her",
            "unboxing a new gaming peripheral at her streaming desk, LED strip lights reflecting off the packaging, genuine excitement on her face",
            "playing a handheld console curled up on a beanbag, fairy lights draped on the wall, cat sleeping beside her",
            "celebrating a tournament win with her team, confetti in the air, stage lights blazing, trophy held high",
            "browsing the aisles of a retro game store, shelves of cartridges and figures surrounding her, nostalgia in the air",
            "streaming a cozy indie game on a rainy evening, chat scrolling on a second monitor, warm drink beside the keyboard",
            "setting up her streaming equipment in her colorful bedroom studio, ring light on, testing the camera angle with a peace sign"
        ],
        "suggestive": [
            "leaning forward toward her gaming monitor in a dimly lit room, RGB underlighting casting colorful shadows across her features",
            "stretching in her gaming chair after a long session, arms above her head, the neon glow contouring her figure",
            "lying on her stomach on the bed playing a handheld console, legs kicked up behind her, fairy lights twinkling",
            "sitting on the desk beside her gaming setup, legs dangling, headset around her neck, monitor light painting her skin",
            "adjusting her webcam for a late-night stream, leaning close to the lens, LED lights creating a soft colorful halo",
            "in a gaming lounge on a leather couch, controller in lap, looking up from under her bangs with a mischievous grin",
            "dancing to victory music in her streaming room, caught mid-spin, RGB lights streaking in the motion",
            "posing for a selfie with her tournament medal, winking at the phone camera, neon signage glowing behind her"
        ],
        "spicy": [
            "on her gaming chair in intimate attire, LED strips painting her skin in shifting pink and purple, headset still on",
            "lying across her bed with controllers scattered around her, monitor glow the only light source, playful and inviting",
            "in her streaming room after hours, ring light still on, sitting on the desk in delicate lingerie, a private stream for one",
            "curled in the gaming chair wearing almost nothing, neon reflections on bare skin, the chat offline, the camera still rolling",
            "kneeling on the bed with her gaming headset on, RGB keyboard casting rainbow light across lace and skin",
            "perched on the windowsill of her apartment, city lights and LED glow competing, wearing something meant for no audience",
            "in the glow of a single monitor in a dark room, the blue light sculpting her figure in intimate detail",
            "sprawled on a bean bag surrounded by plushies and LED candles, wearing a sheer top, controller resting on her bare thigh"
        ],
        "nsfw": [
            "artistic nude bathed in RGB light from her gaming setup, the colorful glow painting abstract patterns across bare skin",
            "on her bed in the soft light of fairy strings and a single monitor, nude and relaxed, controller forgotten beside her",
            "a figure study lit entirely by neon LED strips, the shifting colors creating an almost painterly quality on her bare form",
            "in the gaming chair, fully nude, bathed in the cool blue light of the monitor, an intimate portrait of a private moment",
            "lying on dark sheets with RGB reflections dancing across her body, a modern chiaroscuro in electric color",
            "standing silhouetted against the glow of her triple-monitor setup, the screens casting her nude outline in vivid light",
            "in a steamy bath with LED candles surrounding the tub, her gaming headset hanging on the wall, bare and unwinding",
            "on the floor of her streaming room, nude among scattered plushies and soft blankets, ring light creating a warm halo"
        ]
    },

    "Fitness/Athletic Training": {
        "sfw": [
            "mid-deadlift in a well-equipped gym, chalk dust floating in the overhead lights, muscles engaged, focused determination on her face",
            "running on a coastal trail at sunrise, ocean crashing on the cliffs below, ponytail streaming behind her in golden light",
            "doing box jumps in a CrossFit gym, frozen mid-air, sweat glistening, raw power and control in every line of her body",
            "stretching on a yoga mat in a sunlit home gym, morning light streaming through tall windows, foam roller nearby",
            "shadow boxing in a gritty boxing gym, hands wrapped, heavy bags swinging in the background, intensity in her eyes",
            "at the top of a mountain after a grueling hike, arms raised in victory, panoramic wilderness stretching behind her",
            "doing pull-ups on outdoor monkey bars in a park, morning dew on the grass, determination etched in her expression",
            "cooling down after a workout, sitting on a bench with a water bottle, gym lights catching the sheen of effort on her skin"
        ],
        "suggestive": [
            "pouring water over her head after an outdoor run, droplets cascading down her neck and shoulders, eyes closed in relief",
            "leaning against the boxing ring ropes, unwrapping her hand wraps slowly, sweat-slicked skin catching the overhead light",
            "doing deep stretches on the gym floor, body folded forward, the lines of her athletic figure on full display",
            "standing in front of the gym mirror between sets, checking her form, muscles pumped and defined, confident gaze at her reflection",
            "sitting on a weight bench toweling off, sports bra damp with sweat, abdominal muscles carved and visible",
            "hanging from a pull-up bar, body extended, every muscle group engaged, the frame capturing athletic beauty",
            "in the locker room after training, leaning against the lockers, freshly showered, steam still clinging to the air",
            "rolling out her muscles with a foam roller on the gym floor, back arched, eyes half-closed, body long and lean"
        ],
        "spicy": [
            "in the empty gym after hours, sitting on the bench press in just a sports bra and brief shorts, overhead lights dimmed to amber",
            "in the locker room wearing only a towel, seated before the mirror, post-workout flush coloring her chest and cheeks",
            "on a yoga mat in her home gym wearing minimal workout attire, deep backbend, body arched and glistening with effort",
            "standing under the gym shower, water running over her athletic frame, steam clouding the glass partition",
            "lying back on a weight bench in lingerie, the gym empty and dark except for a single overhead spotlight",
            "in a private training studio, mirrors reflecting every angle, wearing barely-there athletic intimates",
            "stretching in a deep split on the polished gym floor, overhead light casting long shadows, wearing almost nothing",
            "in the sauna after a hard session, wooden bench beneath her, heat flushing her skin, towel loosely draped"
        ],
        "nsfw": [
            "an artistic nude in the empty gym, standing before floor-to-ceiling mirrors, her athletic form reflected infinitely",
            "in the private shower of the training facility, water streaming over defined muscles, steam softening the edges of the frame",
            "a figure study on the boxing ring canvas, nude and powerful, overhead light carving every muscle like a Renaissance sculpture",
            "reclining nude on a weight bench, the stark gym lighting creating dramatic shadows that emphasize her physique",
            "in the sauna, fully nude, wooden slats beneath her, heat-flushed skin glistening, a study in athletic beauty",
            "standing in the locker room, bare and unposed, natural overhead light catching every contour of her trained body",
            "a nude figure study mid-yoga pose on a mat in golden morning light, strength and flexibility in perfect balance",
            "under the outdoor shower at a beachside training facility, nude, water and sunlight painting her athletic form"
        ]
    },

    "Cosplay/Anime": {
        "sfw": [
            "posing at a convention hall beside an elaborate booth display, colorful wigs and props visible, photographers gathered around",
            "in a Japanese garden with cherry blossoms drifting down, standing on a red bridge, perfectly in character",
            "at a cosplay workshop table surrounded by foam armor pieces, paint pots, and a heat gun, focused on her craft",
            "in a neon-lit Tokyo alley at night, anime billboards towering overhead, vibrant and electric atmosphere",
            "seated in a themed maid cafe, frilly decor and pastel walls, holding a heart-shaped dessert plate with a cheerful pose",
            "at an arcade in Akihabara, colorful game cabinets flashing around her, crane machine prizes in hand",
            "in a professional photo studio with colored backdrop paper, mid-pose with a prop weapon, dramatic wind from a fan",
            "walking through a convention floor crowded with cosplayers, her elaborate costume drawing admiring looks"
        ],
        "suggestive": [
            "in a dimly lit bedroom surrounded by anime figures and fairy lights, sitting on the bed in a flirty character-inspired pose",
            "leaning against a locker in a school hallway set, looking back over her shoulder with an anime-style coy expression",
            "in a Japanese bathhouse changing room, wooden shelves and baskets, steam drifting through the scene",
            "posing in a themed photo studio as a catgirl character, arched back, tail swishing, playful and teasing",
            "in a moonlit rooftop scene with city lights below, wind catching her hair, striking a dramatic magical-girl pose",
            "sitting on a windowsill in a dormitory set, legs drawn up, twilight glow mixing with string lights behind her",
            "in an onsen-themed setting wrapped loosely in a towel, cherry blossom petals on the water surface, steam rising",
            "at a shrine at dusk, paper lanterns glowing warmly, posed in a way that blends innocence and allure"
        ],
        "spicy": [
            "in a fantasy bedroom set with sheer canopy drapes, lying on silk in a revealing character costume, soft candlelight",
            "in a Japanese hot spring, water at chest level, bare shoulders visible, lantern light warm on her flushed skin",
            "wearing a daring version of a schoolgirl uniform in a private studio, skirt hiked, thigh-highs, dramatic uplighting",
            "in a dark dungeon set as a succubus character, chains and candles decorating the walls, seductive and powerful",
            "reclining on a futon in a traditional tatami room, wearing a barely-there kimono that has slipped open, lantern glow",
            "in a magical forest set with bioluminescent lighting, wearing a fantasy costume that reveals more than it conceals",
            "on a throne set as a dark queen character, legs crossed, dramatic side lighting, commanding and sensual",
            "in a steamy bathhouse scene, towel barely covering, water droplets on skin, soft focus through rising steam"
        ],
        "nsfw": [
            "an artistic nude in a cherry blossom shower, petals clinging to bare skin, soft pink light creating a dreamlike atmosphere",
            "a fantasy figure study in a magical forest set, nude among bioluminescent mushrooms and fairy lights, ethereal and otherworldly",
            "on silk sheets in a traditional Japanese room, fully nude, golden lantern light painting her skin, sliding doors open to a moonlit garden",
            "a fine-art nude posed as a classical goddess statue in a marble studio set, dramatic directional lighting",
            "in the hot spring completely submerged to the hips, upper body bare, steam and lantern light creating an impressionist scene",
            "nude on a fantasy throne set, body paint suggesting scales or magical markings, dramatic chiaroscuro lighting",
            "lying among scattered cosplay materials and fabric, nude, the creative chaos of the workshop surrounding her like art",
            "a moonlit rooftop scene, nude silhouette against the neon cityscape, wind catching her hair, anime-inspired composition"
        ]
    },

    "Fashion/Haute Couture": {
        "sfw": [
            "striding down a Milan runway with overhead spotlights blazing, the front row a blur of flashing cameras and famous faces",
            "standing in the doorway of a Parisian atelier, bolts of fabric and dress forms visible behind her, timeless elegance",
            "seated front row at a fashion show, legs crossed precisely, sunglasses perched on her nose, exuding critical authority",
            "being fitted by a tailor in a high-ceiling couture studio, pins and measuring tape, mirrors reflecting every angle",
            "leaning against a vintage car on a cobblestone Parisian street, editorial perfection in every detail",
            "walking through the halls of the Met Gala, grand staircase and floral installations framing her entrance",
            "in a designer showroom surrounded by racks of next-season pieces, running her fingers along the fabrics",
            "posing on the rooftop of a Manhattan high-rise, wind catching her hair, the skyline providing a dramatic urban backdrop"
        ],
        "suggestive": [
            "backstage at a fashion show, half-dressed between changes, stylists buzzing around her, caught in a candid moment of beauty",
            "in a fitting room surrounded by mirrors, trying on a dress that clings and drapes in all the right places, evaluating her reflection",
            "reclining on a velvet settee in a boutique hotel, legs extended, the slit of her dress revealing a length of thigh",
            "leaning into the camera in a high-fashion editorial shoot, décolletage prominent, eyes fierce and magnetic",
            "standing in a rain-soaked Parisian street at night, wet fabric adhering to her figure, streetlights creating halos",
            "in a penthouse getting ready for a gala, seated at a vanity in a slip, the city lights behind her, almost ready",
            "at an after-party on a rooftop terrace, dress strap slipping off one shoulder, champagne in hand, untouchable confidence",
            "in a couture atelier wearing an unfinished gown pinned to her body, raw silk and bare skin intermingled"
        ],
        "spicy": [
            "in a luxury hotel suite in just couture lingerie, perched on the arm of a designer chair, editorial lighting from a single softbox",
            "on a chaise longue in a Parisian boudoir, wearing an avant-garde bodysuit that leaves little to imagination, fashion-as-art",
            "in a marble bathroom wearing only a silk robe that has fallen open, reflected in gilded mirrors, Vogue-worthy composition",
            "backstage alone after the show, stripped down to editorial underwear, sitting on a trunk amid garment bags and runway heels",
            "on black satin sheets wearing sheer haute couture lingerie, the lines between fashion photography and boudoir dissolved",
            "standing in a gallery space wearing only body jewelry and sheer fabric, treated as a living art installation",
            "in a designer fitting room, caught between outfits wearing only a thong and heels, mirrors reflecting every angle",
            "draped across a grand piano in a luxury apartment, wearing nothing but a strategically placed couture scarf"
        ],
        "nsfw": [
            "a fine-art nude editorial in a stark white studio, dramatic single-source lighting, the composition worthy of a gallery wall",
            "standing nude in the couture atelier among dress forms and fabric bolts, a living mannequin more beautiful than any creation",
            "on crumpled white linen in a Parisian apartment, fully nude, morning light through tall shuttered windows, effortlessly editorial",
            "a figure study against a massive abstract painting in a gallery, nude body as art among art, curated and intentional",
            "reclining nude on a designer daybed, the clean lines of modern furniture framing her organic curves, architectural beauty",
            "standing before a floor-to-ceiling window in a high-rise penthouse, full nude silhouette against the city, power and vulnerability",
            "in a rain-streaked glass shower, nude, shot through the water-beaded door, fashion-forward composition in every drop",
            "lying nude on a vast expanse of white paper in a photo studio, body as landscape, minimal and breathtaking"
        ]
    },

    "Amateur/Girl Next Door": {
        "sfw": [
            "sitting on the front porch steps of a charming suburban home, lemonade in hand, golden afternoon light filtering through the trees",
            "walking her dog through a tree-lined neighborhood park, autumn leaves crunching underfoot, genuine carefree smile",
            "at a local farmers market browsing fresh produce, canvas bag over her shoulder, weekend morning sunshine all around",
            "in her cozy kitchen baking cookies, flour dusted on her cheek, warm light from the window, the picture of domestic comfort",
            "studying at a coffee shop window seat, laptop and books spread out, rain streaking the glass, lost in concentration",
            "riding a bicycle down a quiet suburban street at golden hour, basket on the handlebars, hair catching the breeze",
            "at a backyard barbecue laughing with unseen friends, fairy lights strung overhead, casual and completely at ease",
            "lounging on a hammock in the backyard reading a book, dappled sunlight through the trees, lazy Sunday energy"
        ],
        "suggestive": [
            "lying on her bed scrolling through her phone, afternoon light slanting through the blinds, looking up with a surprised half-smile",
            "getting ready in her bathroom mirror, fresh from the shower, towel wrapped around her, applying mascara with her lips parted",
            "washing her car in the driveway on a hot day, water splashing back on her, shirt clinging, laughing at the mess",
            "stretching on the couch in the living room, arms above her head, shirt riding up, completely unselfconscious",
            "sitting on the kitchen counter in the morning, legs swinging, coffee mug in hand, sleepy and soft in the early light",
            "trying on outfits in her bedroom, caught between changes, standing in front of the closet mirror in a fitted top and underwear",
            "sunbathing in the backyard on a towel, propped on her elbows, looking over her shoulder toward the camera",
            "lying on the living room floor doing homework, chin on her hands, legs kicked up behind her, the mundane made magnetic"
        ],
        "spicy": [
            "in her bedroom in matching lingerie she clearly just bought, posing in front of the full-length mirror, testing her confidence",
            "in the bathroom with steam from a recent shower, wearing just a towel that is slipping, mirror fogged at the edges",
            "on her bed in an oversized flannel shirt and underwear, laptop pushed aside, looking directly at the camera with newfound boldness",
            "standing in the kitchen doorway in a sheer nightgown, backlit by the warm light of the room behind her",
            "lying on rumpled sheets in a simple lace bralette and cotton underwear, natural and unpolished, bedroom afternoon light",
            "in the laundry room perched on the washing machine in intimate wear, fluorescent light above, unexpectedly sultry",
            "taking a mirror selfie in her bedroom wearing a matching set, phone half-covering her face, playful and real",
            "in the bathtub surrounded by bubbles, one knee drawn up, candle flickering on the ledge, eyes half-closed"
        ],
        "nsfw": [
            "a simple artistic nude on her own bed, afternoon sunlight through cotton curtains, natural and unpretentious beauty",
            "standing nude by the bedroom window, peeking through the curtains at the quiet street, backlit silhouette in soft focus",
            "in the bathtub, water at her hips, no bubbles, candlelight warm on bare skin, intimate and unguarded",
            "lying nude on a blanket in the backyard at night, starlight above, string lights providing gentle warm illumination",
            "a figure study on the living room couch, nude and sprawled comfortably, natural window light, everyday intimacy",
            "in the shower, glass door slightly open, steam and water framing her bare form, completely natural",
            "nude morning stretch in bed, tangled sheets barely covering anything, golden light flooding through sheer curtains",
            "standing in front of the bathroom mirror after a shower, fully bare, towel on the rack, honest and real"
        ]
    },

    "MILF/Mature Latina": {
        "sfw": [
            "in a vibrant outdoor mercado, surrounded by colorful textiles and fresh flowers, selecting fruit with knowing hands",
            "hosting a dinner party in her elegant dining room, candlelight reflecting off wine glasses, commanding the table with warmth",
            "walking through a sunlit courtyard with terra cotta tiles and bougainvillea cascading from the walls, effortless sophistication",
            "at a salsa club seated at the bar, the band playing in the background, watching the dancers with a knowing smile",
            "in her lush home garden tending to tropical plants, afternoon sun warm on her shoulders, peaceful and grounded",
            "at a beach resort sipping a mojito under a palapa, ocean waves rolling in the distance, radiating seasoned confidence",
            "in a professional office leaning against the desk, city view behind her, powerful and polished with maternal warmth",
            "cooking in a beautiful kitchen filled with the aromas of traditional food, warm lighting, generosity in every gesture"
        ],
        "suggestive": [
            "dancing salsa in her living room, hips moving to the music, hair swinging, the room lit by warm lamplight and candles",
            "leaning against the kitchen counter with a glass of red wine, top button of her blouse undone, warmth in her eyes",
            "sitting on the edge of a resort pool, feet in the water, looking back over her shoulder, wet hair clinging to her neck",
            "in front of her vanity getting ready for a date, applying perfume to her wrists, cocktail dress hugging every curve",
            "on the balcony of her apartment at dusk, city lights below, leaning on the railing, the breeze pressing fabric against her body",
            "at a rooftop party, seated with legs crossed, dress riding up her thigh, holding court with magnetic presence",
            "stretching after a morning workout in her home gym, body glistening, mature confidence radiating from every motion",
            "standing in the doorway of her bedroom, hand on the frame, backlit, silhouette suggesting the fullness of her figure"
        ],
        "spicy": [
            "on silk sheets in her candlelit bedroom, wearing lace lingerie in deep red, every curve celebrated, experienced and unapologetic",
            "in a luxury hotel bathroom in a matching lingerie set, mirror reflecting her confident pose, golden light from sconces",
            "reclining on a chaise by the indoor fireplace in a sheer robe, one leg extended, wine glass on the side table",
            "in the master bedroom wearing a corset and stockings, seated at the vanity, applying lipstick with practiced precision",
            "standing in the shower behind frosted glass, steam rising, the outline of her full figure visible, warm and inviting",
            "on the bed with silk pillows, wearing a barely-there negligee, looking into the camera with seasoned seduction",
            "in a private hot tub on a terrace, bikini top discarded beside her, warm water bubbling around her bare shoulders",
            "draped across a velvet sofa in embroidered lingerie, one hand in her hair, firelight flickering across her skin"
        ],
        "nsfw": [
            "an artistic nude on rich burgundy sheets, her mature curves sculpted by warm directional light, confident and timeless",
            "standing nude before a full-length mirror, her body reflected with unflinching honesty, candlelight celebrating every line",
            "in a deep bathtub with rose petals floating on the surface, bare from the waist up, steam softening the frame",
            "reclining nude on a fur throw in front of the fireplace, golden light playing across her skin, Renaissance in spirit",
            "a figure study in her sunlit bedroom, standing by the window, curtains half-drawn, light tracing the topography of her body",
            "on the terrace at night, city below, nude and unhurried, moonlight and warm ambient light painting her skin",
            "in a luxury spa setting, nude on a massage table, warm stones and candles creating an atmosphere of sacred indulgence",
            "lying nude on white linen, tropical flowers scattered around her, natural window light, the embodiment of Latina goddess energy"
        ]
    },

    "Yoga/Wellness/Spiritual": {
        "sfw": [
            "in a tree pose on a cliff overlooking the ocean at sunrise, mist rising from the water, perfect stillness and balance",
            "meditating in a sunlit studio with bamboo floors and hanging plants, incense smoke curling in the golden light",
            "practicing a flowing vinyasa sequence in a Bali rice terrace at dawn, emerald green paddies stretching to the horizon",
            "seated in lotus position on a wooden dock over a still lake, mountains reflected in the water, serene and centered",
            "preparing a herbal tea ceremony in a minimalist kitchen, crystals and dried herbs on the counter, peaceful intention",
            "in a desert landscape doing a warrior pose at sunset, red rock formations behind her, sky ablaze with color",
            "teaching a class in an airy yoga studio, students in soft focus behind her, natural light flooding through skylights",
            "walking barefoot through a dewy meadow at dawn, wildflowers at her ankles, mala beads swaying gently with each step"
        ],
        "suggestive": [
            "in a deep backbend on a yoga mat in golden hour light, spine arched, the pose revealing the full line of her body",
            "practicing a hip-opening pose in a candlelit studio, body folded forward, breath visible in the warm air",
            "in a hot yoga session, skin glistening with perspiration, holding a challenging pose, fabric clinging to every contour",
            "stretching in a splits position on a sunlit balcony, morning dew on the railing, the openness of the pose deeply alluring",
            "emerging from a cenote in the Yucatan, water streaming off her skin, sunlight beaming down through the cave opening",
            "doing an inversion against a studio wall, body inverted and elongated, the world turned upside down, ethereal and strong",
            "lying in savasana on a rooftop at dusk, body fully extended, eyes closed, the sky darkening above her relaxed form",
            "in a seated twist on a beach at sunset, torso rotated, the ocean wind pressing thin fabric against her curves"
        ],
        "spicy": [
            "practicing tantric poses in a candlelit room draped with silk, wearing minimal clothing, spiritual energy palpable in the air",
            "in a private outdoor shower at a jungle retreat, water cascading over her, surrounded by tropical foliage, wearing almost nothing",
            "on a meditation cushion in a dimly lit temple space, wearing only flowing fabric draped across her lap and chest",
            "in a hammock at a wellness retreat, wearing a sheer sarong, body visible through the weave, afternoon light dappled by palms",
            "doing a nude yoga pose in a private studio, the morning sun creating a halo effect, spiritual and sensual intertwined",
            "in a sacred hot spring surrounded by moss-covered rocks, bare shoulders above the steaming water, eyes closed in meditation",
            "lying on a wooden floor in a candlelit room wearing only mala beads, body arranged in a mudra-like posture",
            "in an outdoor bath at an ashram at night, bare under starlight, flowers floating on the water, deeply peaceful and exposed"
        ],
        "nsfw": [
            "a nude figure study in a yoga pose on a cliff at sunrise, her body silhouetted against the fiery sky, spiritual and raw",
            "lying nude on a massage table in a jungle spa, warm oil glistening on her skin, tropical sounds filling the air",
            "a nude meditation in a private garden, seated in lotus, morning light filtering through leaves, body as temple",
            "standing nude under a jungle waterfall, water crashing over her shoulders, surrounded by emerald green, primal and free",
            "in a candlelit room performing a nude backbend, the arch of her body creating a living sculpture of strength and surrender",
            "reclining nude on a bed of flower petals in a temple-inspired setting, incense smoke and golden light, sacred sensuality",
            "a nude figure study in warrior pose on a deserted beach at dawn, sand and sea and skin, elemental and powerful",
            "floating nude in a cenote, crystal-clear water revealing every detail, sunbeams piercing down from the cave above"
        ]
    },

    "Alternative/Tattooed": {
        "sfw": [
            "leaning against a graffiti-covered brick wall in an urban alley, neon signs from nearby bars reflecting off wet pavement",
            "browsing vinyl records at an independent music shop, fingers flipping through the crates, tattoos visible on her forearms",
            "sitting on the steps of a punk venue after a show, cigarette smoke curling, street lights casting long shadows",
            "at a tattoo parlor seated in the artist's chair, fresh ink being applied, needles buzzing, stoic and focused",
            "performing on a small stage at a dive bar, microphone in hand, stage lights cutting through haze, raw energy",
            "walking through an industrial district at dusk, abandoned warehouses and freight trains in the background, boots on gravel",
            "at a motorcycle rally leaning against a vintage chopper, leather and chrome, dusty sunset painting the scene amber",
            "in a dimly lit record store cafe, headphones on, coffee in a chipped mug, lost in the music, tattoos telling stories"
        ],
        "suggestive": [
            "in a dark studio with a single spotlight, tattoos on full display, body turned to show the art covering her back and arms",
            "at a warehouse party, dancing in the haze and colored lights, sweat on her collarbone, fabric shifting with movement",
            "leaning over a pool table in a dive bar, tight top riding up, lower back tattoo visible, looking up with a challenge in her eyes",
            "sitting on the hood of a muscle car at a drive-in movie, legs stretched out, screen light flickering across her inked skin",
            "in an abandoned building, light streaming through broken windows, posing against crumbling brick, body language defiant and alluring",
            "backstage at a concert, perched on an amp, flushed from the crowd, tank top damp, tattoos glistening under fluorescent light",
            "lying on a leather couch in a loft apartment, industrial windows behind her, one arm behind her head revealing a full sleeve",
            "in a rain-soaked alley at night, neon reflecting off wet skin, clothing plastered to her body, unapologetically fierce"
        ],
        "spicy": [
            "in a dark bedroom lit by candles and string lights, wearing black lace lingerie, every tattoo a chapter in the story of her body",
            "in a gritty industrial loft in just underwear and combat boots, tattoo sleeves on display, dramatic side lighting",
            "on a motorcycle in a garage wearing only a leather jacket unzipped over bare skin, grease on her hands, tattoos everywhere",
            "in a dungeon-adjacent space with chains and candles, wearing a harness and little else, tattoos mapping her rebellion",
            "lying on black sheets, tattooed body in lingerie, candles creating warm pools of light against the darkness",
            "in a bathtub filled with dark water, tattoos visible beneath the surface, candles surrounding the tub, gothic and beautiful",
            "standing against a concrete wall in nothing but fishnets and a bralette, graffiti behind her, hard light from one side",
            "in a photographer's industrial studio, wearing sheer black over tattooed skin, the fabric hiding nothing"
        ],
        "nsfw": [
            "an artistic nude on black sheets, every tattoo visible and celebrated, candlelight tracing the ink and the skin beneath it",
            "standing nude in an industrial space with concrete and steel, her tattooed body the most colorful thing in the frame",
            "a figure study in a gritty warehouse, nude among chains and steel beams, dramatic chiaroscuro revealing every inked detail",
            "lying nude on a vintage leather couch, full tattoo coverage on display, window light cutting diagonal shadows across her",
            "in a steamy bathroom, nude, tattoos rendered in sharp detail against wet skin, mirror reflecting the art on her back",
            "a nude portrait in a candlelit gothic bedroom, dark walls, crucifixes and candles, her tattooed form like a profane altar piece",
            "standing at a rain-streaked window, nude silhouette from behind, the tattoos on her back and legs visible in the backlight",
            "on the floor of a converted warehouse studio, nude, industrial fan blowing her hair, the contrast of soft skin and hard ink"
        ]
    },

    "ASMR/Girlfriend Experience": {
        "sfw": [
            "curled up on a plush couch under a knit blanket, fairy lights twinkling behind her, holding a warm mug, whispering comfort",
            "setting up her microphone and triggers on a desk, soft pink lighting, fuzzy items and brushes arranged neatly for a session",
            "reading a book by a rain-streaked window, the patter of drops audible, a candle flickering on the sill, pure coziness",
            "in a cozy kitchen making hot chocolate, marshmallows floating, steam rising, her smile warm enough to melt anything",
            "lying on her stomach on the bed writing in a journal, fairy lights above, soft music implied, gentle and present",
            "walking through a quiet bookstore, fingers trailing along spines, whispering titles, the intimacy of shared silence",
            "on a picnic blanket in a sun-dappled park, preparing a basket of treats, looking up at the camera like greeting someone she loves",
            "in a cozy bedroom recording an ASMR video, headphones on, tapping gently on objects, face close to the mic, soothing presence"
        ],
        "suggestive": [
            "lying on the bed propped on pillows, looking into the camera as if it were a lover's face, whisper-close, eyes soft and inviting",
            "in a bubble bath with candles, leaning on the edge of the tub, chin on her arms, speaking softly to the viewer",
            "brushing her hair in a mirror by candlelight, nightgown slipping off one shoulder, the intimacy of a private grooming ritual",
            "curled on the couch in an oversized sweater and nothing else, legs tucked under her, reaching toward the camera to draw you closer",
            "in bed under the covers, face lit by the phone screen, whispering goodnight, the camera positioned like a face on the pillow beside her",
            "sitting on the bathroom counter in a silk robe, doing her skincare routine, occasionally looking at the camera with gentle affection",
            "leaning very close to the camera with half-lidded eyes, lips barely parted, breathing softly, the microphone catching every whisper",
            "in the kitchen late at night in a thin nightgown, making a midnight snack, lamp light warm on her sleepy features"
        ],
        "spicy": [
            "on the bed in delicate lingerie, whispering to the camera placed on the pillow beside her, fairy lights creating a warm glow",
            "in a candlelit bedroom wearing a sheer babydoll, running her fingers slowly along her collarbone, eye contact unwavering",
            "drawing a bath in lingerie, testing the water with her fingers, steam rising, looking back at the camera with a come-hither gaze",
            "lying on silk sheets in a lace set, tracing patterns on the pillow beside her as if touching someone's face, tender and erotic",
            "in front of her vanity in just a bra, slowly applying body lotion, the mirror doubling the intimate scene",
            "under the sheets with only her face and bare shoulders visible, whispering, the camera impossibly close, pillow-talk intimacy",
            "sitting in the center of the bed in a sheer nightgown, candles everywhere, unwrapping a gift slowly, each gesture deliberate",
            "in a dimly lit room wearing a lace bodysuit, lying on her side, hand outstretched toward the camera, beckoning"
        ],
        "nsfw": [
            "a tender nude in warm candlelight, lying in bed facing the camera as if it were a partner, expression soft and deeply intimate",
            "in the bathtub, water at her waist, bare and unguarded, speaking softly to the viewer, the vulnerability as powerful as the nudity",
            "on white sheets in morning light, nude and half-asleep, reaching toward the camera with a lazy smile, genuine warmth",
            "a nude self-portrait in the bathroom mirror, freshly showered, hair damp, no performance, just honest presence",
            "lying nude under a single sheet that has slipped to her hips, candlelight, looking at the camera with profound tenderness",
            "in the bedroom, nude and kneeling on the bed, hands in her lap, soft lamp light, the intimacy of being truly seen",
            "standing nude by the window at dawn, back to camera, looking over her shoulder, inviting the viewer into her quiet morning",
            "a nude close-up, just her face and bare shoulders on the pillow, eyes open, the most intimate portrait possible"
        ]
    },

    "Dominatrix/BDSM": {
        "sfw": [
            "standing in a gothic-arched hallway of a converted manor, candelabras flickering, her presence commanding the entire corridor",
            "seated on a throne-like chair in a dimly lit parlor, legs crossed, chin lifted, the room bowing to her authority",
            "walking through a high-end fetish club before opening, inspecting the equipment and decor with proprietary satisfaction",
            "in a professional dungeon space adjusting restraints on a St. Andrew's cross, clinical precision, expert hands",
            "at a formal dinner in a candlelit dining room, seated at the head of a long table, guests unseen, queen of her domain",
            "in a dark library with floor-to-ceiling bookshelves, holding a volume on philosophy, leather armchair, intellectual power",
            "standing at the top of a spiral staircase looking down, dramatic overhead light, architecturally framed dominance",
            "in her private chambers organizing an array of finely crafted implements, each one selected with exacting taste"
        ],
        "suggestive": [
            "standing over the camera angle in a dark room, looking down with cool appraisal, a riding crop tapping against her palm",
            "seated on the edge of a desk in her study, legs crossed, one boot dangling, a glass of whiskey in hand, controlled power",
            "in a candlelit dungeon space, pacing slowly, the click of heels echoing, her shadow enormous on the stone wall behind her",
            "adjusting a leather glove in front of a mirror, every motion deliberate, the reflection capturing her from both sides",
            "leaning against a doorframe with arms crossed, the room beyond her dark and mysterious, an invitation and a warning",
            "on a chaise longue in a gothic boudoir, one hand resting on a crop, stockinged legs extended, imperious calm",
            "at the bar of an exclusive club, back to the counter, elbows on the rail, scanning the room like a predator at rest",
            "in her private suite, running her fingers along a shelf of carefully arranged restraints and cuffs, selecting tonight's tools"
        ],
        "spicy": [
            "in the dungeon wearing a leather corset and thigh-high boots, standing beside a bondage bench, single spotlight from above",
            "on the throne in a latex bodysuit, legs spread, riding crop across her thigh, candlelight making the material gleam",
            "in a mirror-walled room wearing a harness and little else, multiple reflections multiplying her commanding presence",
            "bending over a submissive's-eye-view, corset and stockings visible, a chain dangling from her gloved hand",
            "in the candlelit bath chamber, leather and lace barely covering, steam and shadows, the line between pain and pleasure blurred",
            "reclining on a red velvet chaise in a black PVC bodysuit, one leg raised, stiletto heel pointed, dominance at rest",
            "standing in the center of the dungeon in a sheer catsuit, every curve visible, the implements of her trade arranged behind her",
            "at her vanity in the boudoir wearing a corset garter set, applying dark lipstick with surgical precision"
        ],
        "nsfw": [
            "a nude figure study on the throne, bare and more powerful for it, the trappings of authority arranged around her like offerings",
            "standing nude in the dungeon, lit by a single candle, her body radiating authority that needs no costume to enforce",
            "an artistic nude draped over the bondage bench, the contrast of soft bare skin against hard black leather and cold steel",
            "nude except for thigh-high boots and a collar, standing in the mirror room, infinite reflections of uncompromising power",
            "in the bathing chamber, fully nude in a stone tub, candlelight carving shadows across her body, a queen in her element",
            "lying nude on the red velvet chaise, riding crop still in hand, the power dynamic unchanged by the absence of clothing",
            "a dramatic nude portrait against a backdrop of chains and leather, her body the centerpiece, lit like a Baroque painting",
            "standing nude at the dungeon window, moonlight and candlelight competing on her skin, contemplative and absolutely sovereign"
        ]
    },

    "College/Young Adult (18+)": {
        "sfw": [
            "studying at a cluttered dorm desk with textbooks and energy drinks, fairy lights on the wall, laptop stickers visible, focused",
            "walking across a sun-dappled university campus in autumn, fallen leaves swirling, backpack on, heading to class",
            "at a college house party in a living room, red cup in hand, friends blurred in the background, laughing at something off-camera",
            "in a campus coffee shop with earbuds in, notebook open, rain outside the window, the perfect study aesthetic",
            "at a college football game in the stands, face paint on her cheeks, scarf waving, caught mid-cheer",
            "in the university library among towering stacks of books, finding a title on a high shelf, golden afternoon light through tall windows",
            "doing laundry in the dorm basement, sitting on the machine reading a textbook, fluorescent light, mundane and endearing",
            "having a picnic on the campus quad with a blanket and snacks, warm spring day, frisbees flying in the background"
        ],
        "suggestive": [
            "getting ready in the dorm bathroom mirror, hair half-styled, wearing a going-out top, roommate's makeup scattered on the counter",
            "lying on the dorm bed in shorts and a crop top, textbook open but abandoned, looking up from her phone with a playful pout",
            "at a pool party on a hot day, sitting on the pool edge, feet in the water, wet hair pushed back, youth radiating",
            "in the dorm hallway leaning against her door, just come back from a run, flushed and glowing, keys dangling from her hand",
            "doing yoga in her dorm room in tight athletic wear, body stretched in a pose, fairy lights reflected in her eyes",
            "at a sorority event on the dance floor, moving to the music, body caught mid-motion, energy and allure mingling",
            "sitting cross-legged on her bed in an oversized jersey and underwear, laptop open, looking at the camera over the screen",
            "sunbathing on the dorm rooftop in a bikini, textbook propped against her knees, balancing study and relaxation"
        ],
        "spicy": [
            "in the dorm room in lingerie, mirror selfie, phone covering half her face, fairy lights the only illumination",
            "on the unmade dorm bed in a lace bralette and shorts, textbook pushed aside, looking at the camera with newly confident eyes",
            "in the shared bathroom in just a towel, mirror steamed, drawing a heart in the condensation, peeking over her shoulder",
            "lying on the bed in a thin tank top and underwear, laptop light casting blue on her face, late night and uninhibited",
            "at the dorm window in sheer sleepwear, campus lights outside, her reflection ghosting in the glass, between innocence and knowing",
            "sitting on the desk in lingerie, legs crossed, roommate away for the weekend, exploring her confidence in private",
            "on the floor surrounded by polaroid photos, wearing a vintage slip, candle burning illegally in the dorm, intimate and daring",
            "in the closet-sized dorm shower, just a curtain between her and the hallway, steam and soap, the thrill of no real privacy"
        ],
        "nsfw": [
            "a nude self-portrait on the dorm bed, fairy lights above, textbooks still stacked on the nightstand, youthful and brave",
            "standing nude in front of the full-length mirror on the back of the dorm door, morning light, examining herself honestly",
            "in the dorm shower, nude and relaxed, warm water streaming, the small space creating an intimate frame around her body",
            "lying nude on the bed, sheets tangled at her feet, afternoon light through cheap blinds, unfiltered and authentic",
            "a figure study in the window seat of a student apartment, nude, campus visible below, natural light sculpting her young body",
            "nude on the dorm room rug surrounded by study materials, a private moment of freedom between assignments",
            "in the bathroom, nude, towel dropped, looking at herself in the mirror with the curiosity of someone still learning her own beauty",
            "stretched nude across the narrow dorm bed, feet against the wall, the confines of the space making the image more intimate"
        ]
    },

    "MILF/Cougar": {
        "sfw": [
            "on the deck of her beachfront home with a glass of white wine, ocean stretching to the horizon, golden hour light on her face",
            "browsing an upscale boutique, running her fingers along cashmere, shopping bags from designer stores at her feet",
            "at a seaside restaurant, seated at the best table, menu in hand, the kind of woman who never waits for a reservation",
            "walking along a Marina del Rey dock past luxury yachts, sunglasses, confident stride, she owns the boardwalk",
            "hosting a garden party at her elegant home, arranging flowers on the table, effortless hostess energy",
            "at a farmers market in a coastal town, selecting peaches, canvas tote over her shoulder, ageless and beautiful",
            "driving a convertible along the Pacific Coast Highway, wind in her hair, sunglasses catching the light, freedom incarnate",
            "at an art gallery opening, studying a painting with a cocktail in hand, sophisticated and magnetically self-assured"
        ],
        "suggestive": [
            "lounging by her private pool in the late afternoon, sunscreen glistening on her skin, peering over her sunglasses at the camera",
            "in the kitchen pouring wine, leaning against the island counter, dress hugging her hips, looking up with an inviting smile",
            "sitting on the edge of her bed having just kicked off her heels, dress riding up, end-of-evening glow",
            "on the balcony of her beach house at sunset, robe loosely tied, the wind opening it slightly, completely unbothered",
            "getting ready at her vanity, hair half-up, applying lipstick, wearing just a slip, catching the viewer's eye in the mirror",
            "at the pool bar leaning on the counter, swimsuit and sarong, wet footprints on the stone behind her, confidence and allure",
            "reclining on a daybed at a luxury resort, one strap of her sundress fallen, reading a novel, the picture of relaxed sensuality",
            "standing in the doorway of her walk-in closet in a silk camisole, deciding what to wear, the decision itself seductive"
        ],
        "spicy": [
            "on her California king bed in matching silk lingerie, afternoon light through plantation shutters, experienced and magnetic",
            "in the master bathroom, soaking in the tub, candles lit, wine glass balanced on the edge, bare shoulders above the waterline",
            "standing before the bedroom mirror in a corset and stockings, appraising herself with the confidence of a woman who knows her worth",
            "by the pool at night in a sheer cover-up over lingerie, the underwater pool lights casting aqua ripples across her skin",
            "reclining on the chaise in her bedroom in a negligee, reading glasses still on, the intersection of intellectual and sensual",
            "in the outdoor shower of her beach house, water running over her, wearing the minimum, steam rising into the cool evening air",
            "on silk sheets in black lace, one hand tracing her own neckline, the camera capturing the moment from an intimate distance",
            "in the hot tub on her deck at night, bikini top floating beside her, stars overhead, warm bubbles and bare skin"
        ],
        "nsfw": [
            "a nude figure study on the white bed, ocean light flooding the master suite, her mature body celebrated in every ray of sunshine",
            "standing nude at the panoramic bedroom window, the Pacific Ocean behind her, backlit silhouette, timeless beauty",
            "in the outdoor shower fully nude, water cascading, sunset painting her skin in amber, surrounded by tropical plants",
            "reclining nude by the pool at dawn, the still water reflecting her, no one else for miles, serenity and raw beauty",
            "an artistic nude on the living room daybed, floor-to-ceiling ocean views, the composition framing her as part of the landscape",
            "in the master bathtub, water crystal clear, fully nude, candles surrounding the tub, absolute self-possession",
            "nude on the balcony at golden hour, leaning on the railing, wind in her hair, the warm California light worshipping her form",
            "lying nude on the beach at her private stretch of coast, waves reaching her toes, the sand warm beneath her, elemental beauty"
        ]
    },

    "Petite Asian/Feet Content": {
        "sfw": [
            "in a pastel-decorated bedroom sitting at a vanity mirror, cute plushies lined up on the shelf, gentle afternoon light",
            "walking through a cherry blossom park in Tokyo, petals drifting down, a small handbag and cute accessories completing the scene",
            "in a cozy cafe with a matcha latte, seated by the window, feet up on the opposite chair in cute patterned socks",
            "browsing a kawaii accessory shop, holding up earrings to her ears, surrounded by pastels and sparkle",
            "sitting on a park bench removing her shoes, wiggling her toes in the grass, laughing at the sensation, natural and playful",
            "in a bookstore cafe corner, tiny frame curled into an armchair, novel in hand, stocking feet tucked beneath her",
            "at a traditional Japanese tea ceremony, kneeling on tatami, bare feet visible beside her, serene composure",
            "on a bed surrounded by plushies and manga volumes, playing a handheld game, socked feet kicked up behind her"
        ],
        "suggestive": [
            "lying on the bed in thigh-high socks, legs extended toward the camera, toes pointed, emphasizing her petite legs and small feet",
            "sitting on the floor in a short skirt, legs folded beside her, bare feet visible, looking up at the camera from below",
            "in a bubble bath with her feet propped on the edge of the tub, toes peeking through the foam, playful and cute",
            "trying on shoes in a boutique, seated with one foot extended, delicate ankle and arch on display, shoe dangling from her toe",
            "stretching on a yoga mat, bare feet in focus in the foreground, her petite body making long lines, soft studio light",
            "on a bed in a short nightgown, legs drawn up to her chest, bare feet visible, looking over her knees at the camera",
            "sitting on a window ledge barefoot, toes pressed against the glass, rain streaming outside, cozy and flirty",
            "lying on her stomach on a blanket, bare feet raised behind her, anklet catching the light, chin in her hands"
        ],
        "spicy": [
            "on silk sheets in delicate lace lingerie, bare feet pointed toward the camera, toe ring glinting, petite body on full display",
            "kneeling on a bed in a sheer babydoll, feet visible beneath her, ankle bracelet glowing in candlelight",
            "in a steamy bathroom wearing just a towel around her waist, barefoot on wet tile, mirror showing her tiny frame",
            "lying back on cushions in lingerie, one foot raised and resting on her opposite knee, sole toward the camera, intimate lighting",
            "in a dimly lit bedroom in a mesh bodysuit, sitting cross-legged on the bed, bare soles visible, delicate and daring",
            "perched on the bathroom counter in just underwear, feet dangling, toes pointed downward, mirror reflecting her small form",
            "on a chaise in sheer stockings being slowly peeled off, one foot free, the other still encased, lingerie visible above",
            "standing on tiptoes in the bedroom doorway wearing nearly nothing, her small bare feet arched, backlit silhouette"
        ],
        "nsfw": [
            "a nude study on white sheets, her petite body and small bare feet in perfect composition, soft window light, delicate and honest",
            "lying nude on a futon in a tatami room, feet together pointed at the camera, lantern light warm on her diminutive form",
            "in the bath, water clear, fully nude, her small feet visible at the far end of the tub, body submerged to the chest",
            "an artistic nude kneeling on silk, bare feet tucked beneath her, the proportions of her tiny frame a study in delicacy",
            "standing nude before a full-length mirror, her reflection capturing every angle of her petite body, light from a paper lantern",
            "on the bed, nude, feet in the foreground with a shallow depth of field, her face soft-focused but smiling in the background",
            "a nude figure study in a cherry blossom setting, petals on her bare skin and between her toes, ethereal and diminutive",
            "reclining nude on dark sheets, one foot resting on the other, the contrast of her small pale body against the dark fabric"
        ]
    },

    "Latina Curves/BBW": {
        "sfw": [
            "dancing at a vibrant street festival, colorful skirts swirling, music in the air, her curves moving with the rhythm of live drums",
            "at a family-owned bakery selecting pasteles, warm light from the display case, the aroma of fresh bread filling the scene",
            "in a lush tropical garden surrounded by hibiscus and palms, walking along a stone path, hips swaying naturally with each step",
            "at a beach bar watching the sunset, mojito in hand, ocean breeze in her hair, full figure silhouetted against orange sky",
            "in a colorful outdoor market selecting mangoes and papayas, vendors and flowers surrounding her, vibrant and alive",
            "cooking in a warm kitchen, stirring a pot of something fragrant, cumbia playing softly, the heart of the home",
            "sitting on the steps of a colorful colonial building, vivid painted walls behind her, flowers in her hair, magnetic presence",
            "at a dance studio, mid-salsa, caught in motion, her body telling the story the music demands, powerful and graceful"
        ],
        "suggestive": [
            "dancing bachata at a club, body pressed close to the music, curves moving in slow waves, colored lights painting her skin",
            "emerging from the ocean on a Caribbean beach, water streaming over her full figure, sun catching every glistening curve",
            "in a kitchen leaning against the counter, tasting something from a wooden spoon, apron ties accentuating her waist",
            "sitting on a bar stool with legs crossed, dress riding up her thick thighs, looking over her shoulder with a knowing smile",
            "stretching after a dance class, body warm and loose, every curve visible through damp dancewear, powerful and feminine",
            "at a rooftop party at sunset, leaning on the railing, dress caught by the wind, the full geography of her body on display",
            "lying on a pool float, water lapping at her sides, full figure in a swimsuit, sun worshipping without apology",
            "getting ready at her vanity, hair in large rollers, wearing a fitted slip, curves reflected lovingly in the mirror"
        ],
        "spicy": [
            "on satin sheets in bold red lingerie, her voluptuous body arranged like a Renaissance painting, warm lamplight celebrating every curve",
            "in a candlelit bedroom wearing a sheer teddy, full figure visible through the fabric, lying on her side, hand on her hip",
            "in a private jacuzzi, steam rising, wearing a minimal bikini bottom only, water beading on her chest and shoulders",
            "standing before a mirror in a corset that cinches her waist and presents her curves dramatically, candlelight and desire",
            "on a bed of tropical flower petals in lace lingerie, every generous curve adorned, golden skin warm in the soft light",
            "in the shower, water streaming over her full body, wearing nothing but a gold body chain, steam filling the frame",
            "reclining on a velvet sofa in a sheer bodysuit, thick thighs crossed, full breasts prominent, unapologetic abundance",
            "dancing alone in her bedroom in just lingerie, hips moving to an unheard beat, caught in a private moment of self-celebration"
        ],
        "nsfw": [
            "an artistic nude on vibrant fabric, her full Latina curves sculpted by warm directional light, a celebration of abundance",
            "standing nude before a floor-to-ceiling mirror, her voluptuous reflection a monument to body positivity, golden hour light",
            "in a deep bathtub with petals floating on the water, nude from the waist up, her full figure partially visible through clear water",
            "reclining nude on a daybed, every generous curve lit by candlelight, the composition classical and reverent",
            "a figure study outdoors in a private tropical garden, nude among the flowers, her body as lush as the landscape",
            "lying nude on white sheets, the contrast of her golden skin creating warmth, every curve a hill in a beautiful landscape",
            "in an outdoor shower surrounded by jungle foliage, fully nude, water cascading over voluptuous curves, primal and free",
            "on a silk chaise, nude, one arm above her head, the full map of her curves drawn in warm light, unapologetic beauty"
        ]
    },

    "BBW/Southern Charm": {
        "sfw": [
            "on the wraparound porch of a classic Southern farmhouse, rocking chair, sweet tea in a mason jar, fireflies starting to glow",
            "walking through a field of sunflowers at golden hour, the blooms reaching her shoulders, genuine warmth in her smile",
            "at a county fair with cotton candy and a cowboy hat, Ferris wheel lit up behind her, pure Americana joy",
            "in a farm kitchen pulling fresh biscuits from the oven, flour on her apron, checkered curtains, cast iron on the stove",
            "sitting on the tailgate of a pickup truck at sunset, boots dangling, wildflower meadow stretching behind her",
            "at a small-town diner in a vinyl booth, milkshake and jukebox music, neon signs reflecting in the window",
            "picking wildflowers along a country road, gravel path stretching into the distance, rolling green hills on both sides",
            "at a barn dance, clapping along to the fiddle music, string lights overhead, hay bales and laughter all around"
        ],
        "suggestive": [
            "cooling off under a garden hose on a hot summer day, water spraying over her, sundress clinging, laughing and carefree",
            "lying in a hammock on the porch, dress hiked up in the heat, one bare foot hanging over the side, fanning herself lazily",
            "at the lake sitting on the dock, feet in the water, sundress pulled up to her thighs to stay dry, looking over her shoulder",
            "in the farmhouse kitchen in a thin nightgown, morning light through the window, pouring coffee, soft and unguarded",
            "leaning against a hay bale in the barn, shirt tied at her waist, wisps of hay in her hair, warm light filtering through the slats",
            "swimming in a creek on a hot afternoon, emerging from the water, clothes wet and heavy, genuine delight on her face",
            "on the porch swing in the evening, dress strap slipped off her shoulder, firefly light and lantern glow, summer warmth",
            "sitting on the bed in the farmhouse guest room, boots just kicked off, unbuttoning her top button in the heat, ceiling fan spinning"
        ],
        "spicy": [
            "in the farmhouse bedroom in lace lingerie, quilt pushed to the foot of the bed, warm lamplight, full figure celebrated and soft",
            "in the outdoor copper tub behind the farmhouse, bare shoulders above the water, stars overhead, cicadas singing",
            "lying on a vintage quilt in just a cotton bra and panties, bedroom window open, curtain billowing, country heat on her skin",
            "in the barn loft on scattered hay and a blanket, wearing a corset and little else, golden light streaming through gaps in the wood",
            "standing in the kitchen doorway in a sheer nightgown, backlit by warm interior light, full silhouette visible through the fabric",
            "on the four-poster bed in the master bedroom, wearing stockings and a garter, antique lace, the picture of soft Southern seduction",
            "in a vintage claw-foot bathtub, bubbles barely concealing, candles on the window ledge, her full body warm and relaxed",
            "on the porch at night in just underwear and an unbuttoned flannel, the darkness her only audience, lightning bugs and freedom"
        ],
        "nsfw": [
            "a nude figure study on the quilt-covered bed, warm afternoon light through lace curtains, her soft full body honest and beautiful",
            "standing nude in the farmhouse bedroom, full-length mirror reflecting her generous curves, golden light from the window",
            "in the outdoor tub, fully nude, water clear, stars above, the countryside silent around her, completely at peace with her body",
            "lying nude in the hay loft, afternoon sun slanting through the barn boards, her soft skin warm in the dusty golden light",
            "a nude morning portrait by the bedroom window, sheer curtains framing her, every soft curve lit by the gentlest country dawn",
            "in the creek, nude, water to her waist, wildflowers on the bank, sunlight on wet skin, a pastoral Venus",
            "reclining nude on the porch daybed at night, moonlight and firefly glow her only light, Southern summer on bare skin",
            "on white sheets in the farmhouse guest room, fully nude, ceiling fan stirring the air, unpretentious and genuinely lovely"
        ]
    },

    "Black Beauty/Melanin Content": {
        "sfw": [
            "in a sunlit studio with warm wooden floors, natural light catching the richness of her dark skin, surrounded by African art and textiles",
            "walking through a Harlem street market, Kente cloth and gold jewelry catching the sun, confidence in every step",
            "at a rooftop terrace in Lagos at sunset, city lights beginning to glow, her melanin radiant against the amber sky",
            "in a lush botanical garden surrounded by tropical greens, her dark skin a stunning contrast to the vivid foliage",
            "at a natural hair expo, her crown of coils on full display, surrounded by products and community, celebrating beauty",
            "in a gallery of African diaspora art, standing before a large canvas, her presence as striking as anything on the walls",
            "at a book club in a cozy living room, natural light on her face, engaged in conversation, beautiful and brilliant",
            "on a sun-drenched balcony in Accra, traditional beads and gold, the ocean in the distance, queen of her domain"
        ],
        "suggestive": [
            "in a photography studio with dramatic side lighting that sculpts the planes of her dark skin, looking into the camera with intensity",
            "at a pool party, emerging from the water, droplets catching light like diamonds on her melanin-rich skin",
            "in a candlelit room, wearing gold body jewelry that glows against her dark complexion, looking over her shoulder",
            "dancing at a sunset beach party, body caught in motion, the last light painting highlights on her deep skin tone",
            "lying on a daybed in a Moroccan-themed room, body draped in thin fabric, the warm palette complementing her melanin",
            "standing in a rain shower on a warm evening, water streaming over her dark skin, streetlights creating golden highlights",
            "in a luxury spa wearing a wrap, shoulders bare, the contrast of white towel against deep brown skin, relaxed power",
            "getting ready at her vanity, braids being undone, wearing a fitted slip, the ritual of Black beauty captured mid-process"
        ],
        "spicy": [
            "on gold satin sheets in lingerie that contrasts beautifully with her deep skin, candlelight catching gold jewelry and melanin alike",
            "in a luxury bathroom wearing a sheer bodysuit, dark skin visible through the fabric, gold accents everywhere, regal and provocative",
            "reclining on an African-print chaise in delicate lingerie, every shade of her dark skin celebrated in warm lamplight",
            "in a private pool at night, water reflecting city lights onto her bare chocolate skin, wearing barely anything",
            "standing before a gilded mirror in lingerie, her dark body reflected infinitely, gold chains catching the light",
            "on a rooftop at night in a mesh bodysuit, city lights behind her, her melanin absorbing and reflecting the urban glow",
            "in a bedroom draped in earth tones, wearing lace that disappears into her skin tone, candles creating warm pools of light",
            "in the shower, water creating rivers on her dark skin, steam and warm light, the texture of melanin in sharp relief"
        ],
        "nsfw": [
            "an artistic nude on deep blue velvet, her melanin-rich skin glowing under warm studio light, a masterwork in contrast and beauty",
            "standing nude before a window, backlit, the rim of light creating a luminous outline around her dark silhouette, breathtaking",
            "a figure study on white sheets, her deep dark skin the visual anchor, every contour sculpted by golden directional light",
            "in a bath with gold-flecked water, fully nude, her dark body emerging from the surface like a creation myth made visible",
            "reclining nude on African-print fabric, her body adorned only with gold body chains, melanin celebrated in every pixel",
            "a nude portrait in golden hour light, standing in a field, her dark skin absorbing and radiating the warm amber light",
            "lying nude on dark wood floors, her melanin-rich body shot from above, the composition a study in tone and texture",
            "in a candle-filled room, nude and powerful, her dark skin catching every flame, shadows and highlights painting a living masterpiece"
        ]
    },

    "Lesbian/Couples Content": {
        "sfw": [
            "at a cozy cafe sharing a dessert across the table, hands intertwined, city street visible through the steamy window",
            "hiking through autumn woods, walking side by side on a leaf-covered trail, backpacks and matching energy",
            "at a pride event in a joyful crowd, rainbow flags and face paint, arms around each other, celebrating love",
            "cooking dinner together in a warm kitchen, one chopping while the other stirs, domestic harmony, laughter in the air",
            "on a road trip, passenger seat feet on the dashboard, driver laughing, open highway stretching ahead, freedom and partnership",
            "at a farmer's market sharing a bag of fresh peaches, bumping shoulders playfully, Saturday morning togetherness",
            "cuddled on the couch watching a movie, blanket shared between them, popcorn bowl between their laps, quiet contentment",
            "dancing together at a backyard wedding, fairy lights overhead, foreheads touching, the rest of the world blurred away"
        ],
        "suggestive": [
            "slow dancing in the living room in the evening, bodies close, one pair of hands on a waist, the other on a shoulder, intimate sway",
            "at the beach at sunset, applying sunscreen to each other's backs, lingering touches, looking at each other with knowing smiles",
            "in the kitchen, one seated on the counter, the other standing between her legs, cooking paused, tension building",
            "lying face to face on a bed, afternoon light through the curtains, fully clothed but the space between them electric",
            "in a pool together, water to their chests, one pushing wet hair from the other's face, mouths almost touching",
            "getting ready together in the bathroom, one doing the other's makeup, faces very close, the brush paused mid-stroke",
            "in a photo booth, the final frame catching an almost-kiss, the strip of photos a story of escalating desire",
            "sharing a hammock on a lazy afternoon, legs tangled, one reading aloud while the other traces patterns on bare skin"
        ],
        "spicy": [
            "on the bed in lingerie, one straddling the other's lap, foreheads pressed together, hands exploring, candlelight flickering",
            "in the shower together, steam surrounding them, water running over both bodies, one pressed against the tile wall",
            "on a chaise, one lying back while the other hovers above her, lingerie straps being slowly slipped off shoulders",
            "in the bedroom, one unzipping the other's dress from behind, lips on her neck, the dress pooling at her feet",
            "tangled on silk sheets, both in lingerie, legs interlocked, mouths inches apart, the moment before everything",
            "in a bath together, one leaning back against the other, candles lining the tub, hands moving beneath the water",
            "on a hotel bed, one blindfolded in lingerie, the other fully in control, teasing with a feather, sensory anticipation",
            "in front of a mirror, both in intimate wear, one behind the other, arms wrapped around, watching their own reflection"
        ],
        "nsfw": [
            "an artistic nude of two women on white sheets, bodies intertwined, the curves of one flowing into the other, soft morning light",
            "in the shower, both nude, water cascading over entangled bodies, steam softening the frame, raw and tender",
            "a nude figure study of two bodies on a daybed, hands exploring, the composition balanced between intimacy and artistry",
            "on the bed, both nude, one above the other, skin against skin, the warm light catching every point of contact",
            "in a bath together, nude, water clear, their bodies visible and intertwined, candles creating warm reflections on wet skin",
            "lying nude face to face on dark sheets, legs tangled, foreheads touching, the private geography of two women together",
            "a backlit silhouette of two nude figures embracing at a window, the outline of their bodies merged into one form",
            "on a fur throw before a fireplace, both nude, one resting her head on the other's chest, firelight on tangled bodies"
        ]
    },

    "Sexy Japanese Gamer/Competitive Streaming": {
        "sfw": [
            "at a competitive gaming tournament, headset on, focused on the screen, arena lights blazing, crowd energy palpable behind her",
            "in her high-end streaming room, triple monitors glowing, mechanical keyboard and custom controller, RGB lighting pulsing",
            "at a Tokyo arcade, surrounded by rhythm game cabinets, playing with intense precision, neon reflections everywhere",
            "at a gaming convention panel, microphone in hand, speaking to a packed audience, confident and charismatic on stage",
            "unboxing a new graphics card at her streaming desk, genuine excitement, chat scrolling on the second monitor",
            "in a PC gaming cafe in Akihabara, ramen beside her keyboard, late-night session, neon signs outside the window",
            "practicing combos on a fight stick at home, muscle memory drills, focus unwavering, trophies visible on the shelf behind her",
            "doing a meet-and-greet at a convention, signing posters for fans, warm smile, her gaming jersey fresh and crisp"
        ],
        "suggestive": [
            "leaning over her streaming desk adjusting settings, the camera angle looking up at her, monitor light painting her features in blue",
            "stretching in her gaming chair after a long tournament session, arms above her head, body arched, the neon glow contouring her figure",
            "in a hot spring after a tournament trip, steam rising, bare shoulders above the water, mountains visible through the open-air bath",
            "at a cosplay-gaming crossover event, wearing a form-fitting character suit, posing for photographers, fierce and flirty",
            "in her streaming room late at night, oversized jersey slipping off one shoulder, energy drink in hand, drowsy allure",
            "dancing to a rhythm game in her room, body moving precisely, crop top riding up with each motion, LED lights flickering",
            "lying on the bed with her laptop balanced on her stomach, playing a visual novel, legs bent and bare, socked feet in the air",
            "at a pool party with other streamers, rising from the water, wet hair slicked back, competitive confidence translated to physical magnetism"
        ],
        "spicy": [
            "in her gaming chair in lingerie, headset still on, the monitor casting blue and pink light across lace and skin, a private stream",
            "on her bed surrounded by gaming merch and plushies, wearing a sheer gaming jersey over lingerie, controller in her hand",
            "in a themed love hotel room in Tokyo, neon lights and mirrors, wearing barely anything, the aesthetic both playful and provocative",
            "kneeling at her gaming desk in a mesh bodysuit, RGB reflecting off the fabric and her skin, the camera rolling for no audience",
            "in an onsen, standing to leave the water, body steaming, towel in hand not yet wrapped, mountain twilight through the open wall",
            "on silk sheets in a capsule-hotel aesthetic room, neon strip lighting, wearing lingerie with gaming-inspired patterns",
            "in the streaming room after hours, ring light on, wearing a sheer crop top and thong, doing a private cosplay photoshoot",
            "in a glass-walled shower in a high-tech apartment, city of Tokyo visible through the steam, wearing almost nothing"
        ],
        "nsfw": [
            "an artistic nude in her gaming room, RGB lights painting abstract color across bare skin, monitors off, intimate silence",
            "in a Japanese onsen, fully nude, water to her thighs, steam and lantern light creating an impressionist composition",
            "on the bed, nude among scattered gaming peripherals and tangled sheets, monitor glow the only light, private and unfiltered",
            "a figure study in a minimalist Tokyo apartment, nude at the window, neon cityscape below, her reflection ghosting in the glass",
            "in the bath of a luxury ryokan, nude, wooden tub, steam curling, lanterns on the garden wall outside, serene beauty",
            "lying nude on a futon, RGB strip lights on the ceiling creating color bands across her bare body, modern ukiyo-e",
            "standing nude in her streaming room, backlit by the triple monitors, her silhouette crisp and athletic in the electric glow",
            "a nude self-portrait taken with a timer, sitting cross-legged on the gaming chair, headphones on, bare and comfortable in her domain"
        ]
    }
}


# ---------------------------------------------------------------------------
# OUTFIT SETS - suggestive, spicy, nsfw for all 21 niches
# Each niche has 4 outfit descriptions per lane.
# These describe COMPLETE COHERENT LOOKS (not random items).
# ---------------------------------------------------------------------------
GENERATED_OUTFIT_SETS = {

    "suggestive": {
        "Beach/Bikini Lifestyle": [
            "a string bikini with a sheer sarong wrapped low on her hips, sun-warmed skin glistening with coconut oil",
            "a wet white tank top clinging to her curves over bikini bottoms, barefoot on warm sand, hair dripping",
            "a barely-there bikini top with high-cut denim shorts unbuttoned, belly chain catching the light",
            "a backless sundress that hints at everything underneath, wind pressing the fabric against her body"
        ],
        "Equestrian/Country Elite": [
            "fitted riding breeches with a silk blouse unbuttoned to show collarbones, sleeves rolled, tall boots still on",
            "a corseted riding top over jodhpurs, pearl drop earrings, the structured bodice emphasizing her waist",
            "a sheer silk blouse with nothing beneath tucked into high-waisted breeches, riding crop in hand",
            "an off-shoulder cashmere sweater that slips down one arm, paired with fitted trousers and bare feet"
        ],
        "Luxury Travel/Aviation": [
            "a silk slip dress with a plunging back, diamond studs, hotel robe hanging off one shoulder",
            "a fitted business dress with a slit reaching mid-thigh, silk stockings, heels stepping off a jet",
            "a sheer cover-up over a one-piece swimsuit, wet from the infinity pool, designer sunglasses perched on her head",
            "a deep-V wrap dress in champagne silk that opens with every step, gold chain belt resting on her hips"
        ],
        "Gaming/E-Sports (Cute/Casual)": [
            "an oversized cropped gaming jersey with nothing beneath, boy shorts, thigh-high socks with RGB-stripe pattern",
            "a barely-there crop top with her gamer tag, paired with tiny shorts, LED cat-ear headband glowing pink",
            "an unzipped hoodie revealing a lace bralette, paired with cotton panties, fuzzy slippers, headphones around her neck",
            "a tight baby tee featuring an anime print, no bra visible through thin fabric, cute sleep shorts, barefoot"
        ],
        "Fitness/Athletic Training": [
            "a damp sports bra and skin-tight compression shorts, abs glistening with sweat, boxing wraps still on her hands",
            "a mesh-panel sports bra paired with tiny spandex shorts, cross-training shoes, every muscle defined through the fabric",
            "a zip-front sports bra unzipped to the sternum, high-waisted leggings pulled down to hip level, fresh from a run",
            "a racerback tank top cropped to just below the bust, yoga leggings so tight they leave nothing to imagination"
        ],
        "Cosplay/Anime": [
            "a revealing version of a school uniform - shortened plaid skirt, knotted white blouse, thigh-highs with garters peeking out",
            "a skintight catsuit with a plunging neckline, cat ears and tail, thigh-high boots, cosplay-grade detailing",
            "a bikini-armor fantasy outfit with chainmail accents, bare midriff, armored thigh-highs, character-accurate accessories",
            "a barely-there maid outfit with sheer apron, micro skirt, lace headband, thigh-high stockings with ribbon garters"
        ],
        "Fashion/Haute Couture": [
            "a designer bodysuit in stretch mesh under a structured blazer worn with nothing else, stilettos, bold lip",
            "a backless sequin mini dress that dips to her lower back, thigh-high boots, statement choker necklace",
            "a sheer silk blouse completely open over a couture bralette, wide-leg trousers slung low, editorial confidence",
            "a wet-look leather mini skirt with a barely-there bandeau top, runway heels, slicked-back hair"
        ],
        "Amateur/Girl Next Door": [
            "worn-in denim shorts cut very short, a tight white tank top with no bra, barefoot on the kitchen tile",
            "an oversized flannel shirt buttoned only at the center, long bare legs visible, messy morning hair",
            "a sundress with thin straps slipping off one shoulder, backlit so the silhouette of her body shows through",
            "a cropped band tee and cotton underwear, thigh-high socks, sitting on the bed like she forgot you were watching"
        ],
        "MILF/Mature Latina": [
            "a wrap dress in crimson that hugs every mature curve, plunging neckline, gold layered necklaces drawing the eye down",
            "a fitted pencil skirt and sheer blouse, lace bra visible through the fabric, statement earrings, power heels",
            "a body-hugging salsa dress with a dangerous thigh slit, back almost entirely bare, strappy heels",
            "a silk camisole tucked into nothing, worn as a dress, the fabric pooling at mid-thigh, bare legs, gold anklet"
        ],
        "Yoga/Wellness/Spiritual": [
            "a barely-there yoga bra and ultra-low-rise leggings, belly button piercing visible, mala beads on her wrist",
            "a sheer linen wrap worn over a micro bikini, the fabric transparent in the sunlight, barefoot with ankle bracelets",
            "a backless unitard that dips to her tailbone, the pose stretching the fabric taut across her body, spiritual jewelry",
            "a cropped halter top and flowing harem pants worn dangerously low on the hips, gold chain waist belt"
        ],
        "Alternative/Tattooed": [
            "a mesh crop top over a lace bralette, ripped black jeans barely clinging to her hips, every tattoo visible and proud",
            "a vinyl mini skirt with fishnet tights, combat boots, a half-open leather jacket with nothing beneath but inked skin",
            "a band tee slashed to ribbons revealing tattooed skin underneath, black underwear visible at the waistband, choker tight",
            "a corset-style top with lace-up front over tattooed cleavage, micro shorts, thigh-high boots with buckles"
        ],
        "ASMR/Girlfriend Experience": [
            "an oversized boyfriend shirt hanging to mid-thigh with nothing beneath, one shoulder exposed, sleepy bedhead, bare legs",
            "a silk camisole and matching shorts in blush pink, hair loose and tousled, barefoot, reaching toward the camera",
            "a sheer white nightgown that becomes transparent in the lamplight, lace trim, bare feet on soft carpet",
            "a fuzzy cropped sweater falling off both shoulders, cotton panties, cozy socks, curled on the couch"
        ],
        "Dominatrix/BDSM": [
            "a structured black corset over fitted pants, thigh-high stiletto boots, leather gloves, choker with an O-ring",
            "a PVC catsuit with a front zipper pulled down to the sternum, sleek ponytail, riding crop in hand",
            "a leather pencil skirt with a sheer black blouse, visible bra harness underneath, pointed-toe boots, dark nails",
            "a full latex bodysuit in deep red, opera-length gloves, spiked collar, stilettos that could weaponize a glance"
        ],
        "College/Young Adult (18+)": [
            "a cropped school sweater worn braless, plaid mini skirt, knee-high socks, the schoolgirl look turned dangerous",
            "a sheer white top over a bright-colored bralette, low-rise jeans, belly button ring, youthful and bold",
            "a tiny going-out dress, clearly no room for anything beneath it, strappy heels, glitter on her collarbones",
            "an oversized jersey as a dress with nothing underneath, bare legs to her thighs, messy bun, freshly showered"
        ],
        "MILF/Cougar": [
            "a silk wrap dress that opens dangerously low, toned legs visible through the slit, simple gold jewelry, confident poise",
            "a fitted one-piece swimsuit cut high on the hips, sheer wrap around her waist, wet hair, ageless allure",
            "a cashmere V-neck worn without a bra, the softness barely concealing, paired with tailored shorts, barefoot elegance",
            "a satin slip dress in champagne that follows every curve, thin straps, bare back, heels held in one hand"
        ],
        "Petite Asian/Feet Content": [
            "a cropped baby tee with a short pleated skirt, no stockings, bare legs and feet in delicate ankle-strap heels",
            "an oversized shirt barely covering her bottom, bare legs emerging endlessly from the hem, cute toe ring visible",
            "a tiny bikini top and micro skirt showing her petite proportions, barefoot with an anklet, hair in twin tails",
            "a sheer babydoll top over a mini skirt, knee-high socks being slowly pulled down, revealing delicate feet"
        ],
        "Latina Curves/BBW": [
            "a bodycon dress in hot pink that celebrates every curve, plunging neckline, gold hoop earrings, strappy heels",
            "high-waisted jeans painted on, a crop top that ends below the bust, belly out, bold red lip, unapologetic curves",
            "a form-fitting one-piece swimsuit with strategic cutouts, wet from the pool, curves glistening, cover-up draped over one arm",
            "a bandage dress in red that leaves nothing to the imagination, gold body chain visible at the neckline, killer heels"
        ],
        "BBW/Southern Charm": [
            "a gingham sundress unbuttoned one too many, lace bra peeking out, cowboy boots, hair in loose curls",
            "daisy dukes and a knotted plaid shirt, ample cleavage framed by the knot, barefoot in the grass, sun-kissed",
            "a thin cotton nightgown that clings in the summer heat, barefoot on the porch, silhouette visible against the porch light",
            "a fitted sundress with spaghetti straps straining over full curves, no bra, pearl stud earrings, wholesome yet provocative"
        ],
        "Black Beauty/Melanin Content": [
            "a gold mesh top over a black bralette, the metallic fabric stunning against her dark skin, fitted leather pants, heels",
            "a white bodycon dress creating dramatic contrast with her deep melanin, every curve emphasized, gold accessories gleaming",
            "a cropped African-print top with a matching high-slit skirt, waist beads visible at her hip, barefoot on warm wood",
            "a sheer black bodysuit under an open silk robe, gold body chains layered on dark skin, powerful and alluring"
        ],
        "Lesbian/Couples Content": [
            "a fitted tank top with no bra, boxer briefs peeking above low-slung joggers, sporty and subtly provocative",
            "a sports bra and board shorts, freshly surfed, saltwater still dripping, lean body on display",
            "a button-up shirt open to the navel over a bralette, slim jeans, clean sneakers, confident tomboy energy",
            "a cropped hoodie with nothing beneath and fitted shorts, toned midriff visible, athletic watch, effortlessly sexy"
        ],
        "Sexy Japanese Gamer/Competitive Streaming": [
            "a cropped gaming jersey knotted at the ribs over a lace bralette, tiny shorts, thigh-high socks, headset around her neck",
            "a sheer oversized tee with her streaming logo, clearly braless, paired with micro shorts, gaming slippers",
            "a competitive swimsuit for a pool-stream collab, wet fabric clinging to her athletic frame, goggles on her head",
            "a tight cosplay bodysuit from her favorite game character, zipper pulled down to mid-chest, controller in hand"
        ]
    },

    "spicy": {
        "Beach/Bikini Lifestyle": [
            "delicate lace lingerie in ocean blue, the fabric barely covering, silk and skin catching the soft coastal light",
            "a micro bikini with string ties, the triangles minimal, a sheer pareo loosely draped and slipping from her hips",
            "a see-through mesh cover-up over nothing, the fabric wet and transparent, clinging to every curve",
            "a thong bikini bottom with the top untied and held against her chest, tan lines and salt-kissed skin"
        ],
        "Equestrian/Country Elite": [
            "a vintage riding corset in black leather with silk stockings and garter, tall boots still laced, pearl choker at her throat",
            "an open silk robe revealing a lace teddy beneath, riding gloves still on, firelight through the fabric",
            "a sheer French lace bodysuit with nothing beneath, paired with riding boots, crop in hand, aristocratic command",
            "a satin and lace bra set in deep burgundy, garter belt, stockings, her signature pearls the only other adornment"
        ],
        "Luxury Travel/Aviation": [
            "a sheer negligee in champagne silk, open hotel robe barely clinging to her shoulders, city lights behind her",
            "a couture lingerie set in midnight blue with gold hardware, silk stockings, designer heels, first-class elegance stripped down",
            "a barely-there bodysuit in mesh and lace under an open silk kimono, penthouse window framing the skyline",
            "a thong and delicate bralette in ivory lace, hotel bathrobe pooled at her elbows, diamond earrings still on"
        ],
        "Gaming/E-Sports (Cute/Casual)": [
            "a sheer mesh bodysuit with gaming-inspired prints, controller in hand, RGB light painting the transparent fabric in color",
            "a lace bralette and tiny cotton panties in pastel colors, oversized headphones on, thigh-high stockings with bows",
            "a see-through gaming jersey over a micro bikini, LED cat ears glowing, bare legs tucked under her in the gaming chair",
            "a barely-there cosplay lingerie set themed after her favorite character, cat-paw gloves, collar with a bell"
        ],
        "Fitness/Athletic Training": [
            "a strappy sports bra that functions as lingerie, matching micro shorts, sweat still glistening, in the empty gym after hours",
            "a mesh athletic bodysuit that reveals everything beneath, cross-training shoes still on, muscles pumped and defined",
            "just boxing hand wraps and a thong, standing at the heavy bag, every muscle carved and visible, sweat on bare skin",
            "a zip-front sports bra fully unzipped and a tiny athletic thong, body oiled, competition-ready but for a different audience"
        ],
        "Cosplay/Anime": [
            "a lingerie version of a magical girl costume, sheer fabric and ribbons barely covering, wand prop in hand, thigh-highs with garters",
            "a see-through maid outfit with nothing beneath, micro apron, lace headband, collar with a bow, thigh-high stockings",
            "a bondage-inspired catgirl harness with ear headband, tail plug visible at the waistband, paw-print pasties, collar and leash",
            "a sheer kimono open over a micro thong, obi tied loosely at the waist, traditional hair ornaments, bare skin visible everywhere"
        ],
        "Fashion/Haute Couture": [
            "a couture lingerie set with architectural boning and sheer panels, barely-there thong, runway heels, editorial severity",
            "a completely sheer haute couture bodysuit, every line of her body visible, statement jewelry the only opacity",
            "a designer bra and suspender belt in black lace, silk stockings, pointed stilettos, fashion-forward even in undress",
            "a draped silk scarf strategically wrapped as the only garment, haute couture jewelry, the boundary of fashion and nudity"
        ],
        "Amateur/Girl Next Door": [
            "a simple matching bra and panty set from a department store, everyday lingerie that's sexy in its ordinariness",
            "an old oversized t-shirt pulled up to reveal a plain cotton thong, no bra, the casual intimacy of a real bedroom",
            "a see-through nightgown bought on impulse, still with the tag, trying it on in the mirror, nervous confidence",
            "boy shorts and a thin ribbed tank top with nothing beneath, the outline of everything visible, sitting on the bed naturally"
        ],
        "MILF/Mature Latina": [
            "a deep red lace corset with matching thong, garter belt holding sheer stockings, gold jewelry still on, experienced glamour",
            "a sheer black bodysuit that shows everything, gold body chain at her waist, heels, the confidence of a woman who owns her desire",
            "a satin and lace teddy in jewel green, cut high on the thighs, the fabric barely containing her mature curves",
            "just a thong and her signature gold hoop earrings, standing with one hand on her hip, firelight on Latina skin"
        ],
        "Yoga/Wellness/Spiritual": [
            "a sheer yoga wrap draped over bare skin, mala beads the only other adornment, the fabric translucent in candlelight",
            "body paint in sacred geometric patterns covering her otherwise bare form, a living mandala in warm studio light",
            "a micro bikini made of natural fabric and hemp cord, spiritual symbols tattooed or drawn on her skin, barefoot and grounded",
            "just flowing silk scarves wrapped loosely around her hips and chest, the fabric shifting with every breath, incense smoke curling"
        ],
        "Alternative/Tattooed": [
            "a leather harness over bare tattooed skin, matching leather thong, combat boots, studded collar, dark eyeliner smudged",
            "a mesh bodysuit ripped at strategic points, every tattoo visible through the fabric, fishnet stockings, platform boots",
            "a lace-up leather bralette and matching bottoms, tattoo sleeves in full display, chain belt, spiked bracelet",
            "just fishnet tights over a thong, bare tattooed torso, suspenders hanging at her sides, nipple piercings visible"
        ],
        "ASMR/Girlfriend Experience": [
            "a sheer lace babydoll that hides nothing, matching thong, hair down and tousled, candlelight, the camera close enough to whisper to",
            "just a pair of lace panties, hair falling over bare chest, kneeling on the bed, hands reaching toward the camera",
            "a completely transparent nightgown, backlit by lamplight, every line of her body a gentle invitation",
            "silk panties and nothing else, lying on her stomach on white sheets, chin on her arms, looking at the camera with tenderness"
        ],
        "Dominatrix/BDSM": [
            "a full leather harness with strategic openings, thigh-high stiletto boots, opera gloves, spiked collar, riding crop",
            "a latex thong and matching bra, PVC thigh-highs with stiletto heels, leather cuffs on both wrists, chain leash in hand",
            "a sheer black catsuit with a crotch zipper, corset cinching her waist, platform boots, a crop in her teeth",
            "just a leather waist cincher and thong, thigh-high boots with extreme heels, a flogger draped over her shoulder"
        ],
        "College/Young Adult (18+)": [
            "a lace bralette and matching thong in school colors, knee-high socks, hair in pigtails, textbook held strategically",
            "a sheer baby tee worn without a bra over tiny cotton panties, belly button ring, barefoot on the dorm carpet",
            "a barely-there teddy in pink satin, sitting on the unmade dorm bed, fairy lights the only illumination",
            "just an unbuttoned oversized shirt slipping off both shoulders, revealing a lace thong, dorm room chaos behind her"
        ],
        "MILF/Cougar": [
            "a luxurious silk and lace lingerie set in black, garter belt and stockings, confident in the way only experience allows",
            "a sheer robe open over a lace bodysuit, wine glass in hand, the view from the bedroom window stretching to the ocean",
            "a satin corset and matching thong in champagne, bare legs, heels kicked off beside her, mature elegance undressed",
            "just a pair of silk panties and reading glasses, topless but casual about it, sitting up in bed with a book"
        ],
        "Petite Asian/Feet Content": [
            "a micro lingerie set in baby pink with ribbon ties, bare feet with a delicate toe ring, anklet with a tiny bell",
            "a sheer babydoll that barely covers her tiny frame, matching thong, barefoot, toes pointed, full body visible and petite",
            "just thigh-high stockings being peeled off slowly, one foot bare and arched, the other still encased in sheer nylon",
            "a mesh bodysuit that shows her entire small frame, no underwear beneath, barefoot, ankle bracelet, hair ribbons"
        ],
        "Latina Curves/BBW": [
            "a red lace corset that cinches her waist and pushes up her full bust, matching thong, gold body chain, heels",
            "a sheer mesh teddy that leaves nothing to imagination, every curve visible through the fabric, gold hoop earrings",
            "a strappy lingerie set with criss-cross detailing across her full hips and bust, garter clips, stockings rolled down",
            "just a thong and statement gold necklace, standing proud, her voluptuous body adorned only in confidence and jewelry"
        ],
        "BBW/Southern Charm": [
            "a vintage-style lace bra and high-waisted panty set in cream, garter belt, soft curves celebrated in warm cotton and lace",
            "a sheer cotton nightgown unbuttoned to the navel, soft belly and full breasts visible, pearl studs, bare feet on wood floor",
            "a satin corset in dusty rose that gathers and presents her generous figure, matching panties, bare feet, hair down",
            "just a pair of cotton panties and an unbuttoned flannel held closed by one hand, the other brushing hair from her face"
        ],
        "Black Beauty/Melanin Content": [
            "a gold lace lingerie set that glows against her deep dark skin, body chain in gold, the contrast breathtaking",
            "a sheer white bodysuit over her melanin-rich skin, every curve visible through the fabric, gold accessories, heels",
            "a harness-style bralette and matching thong in metallic gold, her dark skin the canvas, dramatic and editorial",
            "just waist beads and a silk thong, her rich melanin the most stunning adornment, standing in warm golden light"
        ],
        "Lesbian/Couples Content": [
            "a sports bra and boxer briefs in black, athletic body on display, confident stance, the simplicity itself seductive",
            "a lace bralette under an open flannel shirt, fitted briefs, one thumb hooked in the waistband, relaxed confidence",
            "a strappy harness over a fitted tank top, brief underwear, the suggestion of what comes next, boots still on",
            "just tight black briefs and bare chest bound with a simple wrap, androgynous beauty, direct eye contact"
        ],
        "Sexy Japanese Gamer/Competitive Streaming": [
            "a sheer gaming jersey over a micro bikini, headset on, thigh-high socks with controller-button patterns, barefoot",
            "a lace bodysuit in neon pink under an unzipped hoodie, gaming slippers, the outfit glowing in RGB monitor light",
            "a cosplay lingerie set themed after a fighting game character, fishnet arm sleeves, platform boots, fierce pose",
            "just tiny shorts and nipple tape with gaming controller icons, headphones on, bare legs folded in the gaming chair"
        ]
    },

    "nsfw": {
        "Beach/Bikini Lifestyle": [
            "bare skin, natural and sun-kissed, her body adorned only by tan lines and a delicate gold anklet",
            "completely nude except for a belly chain, sand on her skin, the ocean her only backdrop",
            "fully bare, wet from the ocean, water droplets the only adornment, sunlight making her skin glow",
            "nude with a sheer sarong draped loosely in one hand but covering nothing, windswept and free"
        ],
        "Equestrian/Country Elite": [
            "fully nude except for her signature pearl necklace, her aristocratic bearing unchanged, firelight on bare skin",
            "bare and regal, tall riding boots the only remaining garment, riding crop in hand, commanding even in nudity",
            "completely nude on the silk sheets, only her pearl earrings remaining, the portrait of old-money sensuality",
            "bare skin adorned with nothing but the gold signet ring she never removes, standing with quiet authority"
        ],
        "Luxury Travel/Aviation": [
            "fully nude in the hotel suite, nothing but diamond stud earrings, the city skyline her outfit",
            "completely bare, wrapped only in the curtain of a floor-to-ceiling window, penthouse view behind her",
            "nude and unhurried, a silk robe discarded beside her on the hotel bed, room service tray untouched",
            "bare skin in the luxury rain shower, nothing adorning her but water and steam, glass and marble framing"
        ],
        "Gaming/E-Sports (Cute/Casual)": [
            "nude except for her gaming headphones still on, RGB light painting color across bare skin, playful and unguarded",
            "completely bare, sitting in the gaming chair, monitor glow the only illumination on her nude form",
            "fully nude among plushies and LED lights, the contrast of soft girlish decor and bare adult body",
            "bare skin bathed in neon monitor light, controller resting on her bare thigh, casual nudity in her element"
        ],
        "Fitness/Athletic Training": [
            "fully nude, every trained muscle visible, standing in the gym mirror, the culmination of discipline made flesh",
            "bare skin glistening with residual sweat, nude on the gym floor, athletic body in sharp anatomical detail",
            "completely nude except for boxing wraps on her hands, the contrast of fierce protection and total vulnerability",
            "nude and powerful, standing under the gym shower, water running over defined shoulders and sculpted legs"
        ],
        "Cosplay/Anime": [
            "fully nude with only character-themed body paint, the artwork covering her skin replacing any costume",
            "bare except for a hair ribbon and thigh-high stockings, the anime-inspired accessories contrasting with real nude beauty",
            "completely nude among scattered costume pieces and wigs, the character shed, the real woman revealed",
            "nude with fantasy body paint suggesting scales or magical markings, her body the canvas for living art"
        ],
        "Fashion/Haute Couture": [
            "fully nude except for a pair of statement runway heels, the fashion reduced to its most minimal expression",
            "completely bare, draped only in a length of uncut couture fabric, held but not wrapped, editorial nudity",
            "nude and statuesque, wearing only an architectural necklace, her body the ultimate garment",
            "bare skin, the haute couture discarded in a pile beside her, her nude form more striking than any design"
        ],
        "Amateur/Girl Next Door": [
            "fully nude on her own bed, nothing fancy, afternoon light through cotton curtains, real and unpretentious",
            "bare skin, no adornment, standing naturally in her bathroom, the everyday honesty of ordinary nudity",
            "completely nude except for a simple necklace she never takes off, sitting on the couch, unselfconscious",
            "nude and freshly showered, towel dropped on the floor, standing in the hallway, caught between rooms"
        ],
        "MILF/Mature Latina": [
            "fully nude, her mature body adorned only by gold jewelry, standing with the confidence of lived experience",
            "completely bare, gold hoop earrings the only detail, her Latina curves a landscape of warm skin and power",
            "nude except for a waist chain in gold, lying on silk, every line of her experienced body lit by candlelight",
            "bare skin, no costume or pretense, her mature curves celebrating every year, fierce and unapologetic"
        ],
        "Yoga/Wellness/Spiritual": [
            "fully nude in a yoga pose, her body the temple itself, mala beads the only adornment, spiritual nakedness",
            "completely bare except for body paint in sacred geometric patterns, the art transforming nudity into ritual",
            "nude and cross-legged in meditation, incense smoke curling around her, bare skin and bare spirit aligned",
            "bare, standing under a waterfall in nature, wearing only a flower tucked behind her ear, primordial and clean"
        ],
        "Alternative/Tattooed": [
            "fully nude, her tattoos the only covering, every piece of ink visible from head to toe, the body as gallery",
            "bare skin covered in tattoo art, only a choker necklace remaining, combat boots kicked off beside her",
            "completely nude except for her piercings, the metal catching candlelight, tattooed skin in sharp detail",
            "nude and defiant, standing in hard industrial light, her inked body a declaration, nothing hidden"
        ],
        "ASMR/Girlfriend Experience": [
            "fully nude under the sheets with just her face and bare shoulders visible, whispering, intimate and close",
            "completely bare, lying on the bed facing the camera, the nudity tender rather than performative, morning light",
            "nude and fresh from the bath, towel dropped, standing close to the camera, the intimacy of being fully known",
            "bare skin, nothing between her and the viewer, kneeling on the bed, arms open, the ultimate vulnerability"
        ],
        "Dominatrix/BDSM": [
            "fully nude except for thigh-high boots and a leather collar, still radiating absolute command and control",
            "completely bare but holding a riding crop, the power dynamic untouched by the absence of clothing",
            "nude with just leather cuffs on her wrists and a chain belt, her authority inherent, not costume-dependent",
            "bare skin, the implements of her trade arranged around her like a queen's regalia, nudity as power"
        ],
        "College/Young Adult (18+)": [
            "fully nude on the dorm bed, fairy lights above, textbooks nearby, youthful body in honest natural light",
            "completely bare, standing at the dorm mirror, the unselfconscious nudity of someone discovering their beauty",
            "nude and relaxed, wrapped in nothing but the confidence of youth, sitting on the floor surrounded by pillows",
            "bare skin in morning light through cheap blinds, the dorm room mundane, her nude body the only point of beauty"
        ],
        "MILF/Cougar": [
            "fully nude, her mature body bathed in California golden light, nothing but confidence and a knowing smile",
            "completely bare, a glass of wine in hand, seated on the bed, the casual nudity of a woman at total ease",
            "nude and ageless, standing by the pool at dawn, the water reflecting her bare form, earned beauty on display",
            "bare skin, reading glasses still on, nude in bed, the unapologetic nakedness of a woman who needs no costume"
        ],
        "Petite Asian/Feet Content": [
            "fully nude, her tiny frame completely bare, delicate toe ring and anklet her only adornments, soft light",
            "completely bare, petite body on white sheets, bare feet pointed, every small detail of her form visible",
            "nude except for an ankle bracelet, lying with feet toward the camera, her small bare soles in the foreground",
            "bare skin, diminutive and delicate, standing on tiptoes, her entire petite nude form captured in gentle light"
        ],
        "Latina Curves/BBW": [
            "fully nude, every voluptuous curve on display, adorned only by gold waist beads, proud and powerful",
            "completely bare, her full Latina figure lit by warm directional light, curves celebrated without restraint",
            "nude except for statement gold earrings, her generous body unapologetic and magnificent in candlelight",
            "bare skin, curves and softness everywhere, lying on vibrant fabric, a fertility goddess in living color"
        ],
        "BBW/Southern Charm": [
            "fully nude, soft curves in gentle country light, her generous body natural and unpretentious, pearl studs her only jewelry",
            "completely bare, standing in golden farmhouse window light, every soft curve honest and beautiful",
            "nude and comfortable, her full figure on a vintage quilt, the authenticity of a real body in real light",
            "bare skin, nothing but warmth and generosity in her form, wildflower tucked behind her ear, Southern simplicity"
        ],
        "Black Beauty/Melanin Content": [
            "fully nude, her deep melanin glowing under warm light, gold body chain the only adornment, a queen unveiled",
            "completely bare, her dark skin stunning against white sheets, the contrast itself a work of art, golden highlights",
            "nude except for gold waist beads traditional to her heritage, her melanin-rich body a celebration of Black beauty",
            "bare skin, rich and dark and radiant, standing in a single beam of golden light, every tone of her melanin visible"
        ],
        "Lesbian/Couples Content": [
            "fully nude, athletic body on display, lean and strong, the simple confidence of being bare and unashamed",
            "completely bare, lying on the bed, body open and relaxed, nothing between skin and the sheet beneath",
            "nude and natural, the body of someone comfortable in their skin, soft light on bare form, unpretentious beauty",
            "bare skin, strong shoulders and gentle curves, standing at the window, backlit nude silhouette, quiet power"
        ],
        "Sexy Japanese Gamer/Competitive Streaming": [
            "fully nude except for her gaming headset, sitting in the chair, monitor light on bare skin, her most private stream",
            "completely bare, lying on the bed among gaming peripherals, nude body bathed in RGB light, digital and organic merged",
            "nude in the bath of a traditional ryokan, wooden tub, steam, her competitive edge softened into serene bare beauty",
            "bare skin in neon monitor glow, nude and cross-legged in the gaming chair, headphones on, totally in her element"
        ]
    }
}
