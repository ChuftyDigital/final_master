# Premium FLUX Prompt System - Complete Guide

## Overview

I've created a **cinema-grade prompt generation system** that produces extremely detailed, professional-quality prompts specifically optimized for FLUX.1. This ensures your reference images will be photorealistic with exceptional detail.

---

## What's New

### 1. **Premium Prompt Generator** (`scripts/generate_premium_prompts.py`)
Creates prompts with:
- **Detailed physical descriptions** (height, build, hair, eyes, skin)
- **Professional lighting specifications** (Rembrandt, studio, natural window)
- **Camera settings** (Sony A7R IV, Zeiss 85mm f/1.8 at f/2.0)
- **Technical details** (ISO 100, 1/160s, 5600K color temp)
- **Composition guidelines** (rule of thirds, framing, posing)
- **Atmosphere and style descriptions**
- **Critical quality requirements** for natural skin texture

### 2. **Premium Workflow** (`workflows/flux_premium_automated_generator.json`)
Full automation that:
- Loads prompts from `input/prompts_premium_*.txt` files
- Uses WAS Node Suite for file-based automation
- Generates all 3 images per character automatically
- Saves with correct filenames

### 3. **Generated Files**
- `input/prompts_premium_front.txt` - 21 front-facing portraits
- `input/prompts_premium_angle.txt` - 21 three-quarter angles
- `input/prompts_premium_natural.txt` - 21 natural expressions
- `input/prompts_premium_index.txt` - Complete character index

---

## Prompt Quality Comparison

### BASIC PROMPT (Old)
```
Professional portrait photograph of ISABELLA REYES, a 26-year-old 
Latina woman from Colombian heritage. 5'6" tall with slim build. 
Dark brown long straight hair, brown almond eyes, warm olive skin. 
Front-facing portrait, soft studio lighting, photorealistic 8k.
```
**Word count:** ~50 words
**Detail level:** Basic

---

### PREMIUM PROMPT (New)
```
Subject: Professional portrait photograph of ISABELLA REYES, a 26-year-old 
Latina woman with Colombian heritage.

Physical Description: She stands 5'6" tall with a slim build with feminine curves. 
Her hair is dark brown in color, long in length and straight in texture, cascading 
down past her shoulders, flowing naturally with subtle movement. Her eyes are brown 
and almond-shaped, deep and expressive with warm undertones, drawing attention with 
their natural allure. She has a warm olive complexion that glows with natural 
radiance and health. Her face has an oval with defined features, creating a 
naturally photogenic silhouette.

Composition: Classic head-and-shoulders portrait with ISABELLA REYES positioned 
squarely facing the camera, shoulders aligned with the frame. The composition 
follows the rule of thirds with eyes positioned along the upper horizontal third 
line, creating a naturally engaging focal point. The frame captures from mid-chest 
upward, providing context while keeping focus on facial features. Head is straight 
with minimal tilt, creating a sense of directness and confidence. Expression is 
neutral with a soft, natural smile - lips gently closed, eyes alert and engaged 
with the camera. This frontal approach creates the most accurate representation 
for facial recognition and reference purposes.

Lighting: Soft diffused studio lighting setup with a large octagonal softbox 
positioned directly in front and slightly above eye level, approximately 45 degrees 
from camera axis. A white reflector positioned below chin level provides subtle 
fill, eliminating harsh shadows while maintaining natural dimensionality. The key 
light creates gentle, flattering illumination that emphasizes cheekbones without 
creating deep shadows. Color temperature is calibrated to 5600K daylight balance, 
ensuring accurate skin tone reproduction. Background receives minimal light, 
creating subtle separation between subject and backdrop.

Technical Specifications: Captured with professional-grade equipment using a 
Sony A7R IV full-frame mirrorless camera paired with a Zeiss Batis 85mm f/1.8 
lens, the gold standard for portrait photography. The lens is set to f/2.0 to 
create a beautifully shallow depth of field that isolates the subject from the 
background while maintaining tack-sharp focus on the eyes. ISO is set to 100 
for maximum image quality and dynamic range. Shutter speed is 1/160s to eliminate 
any motion blur while maintaining natural appearance.

The image is rendered in photorealistic 8K resolution with exceptional detail 
in every element - individual strands of hair, the subtle texture of skin with 
visible pores and natural imperfections, fine details in fabric and accessories. 
The color grading maintains natural skin tones with subtle warmth, professional 
contrast that adds depth without looking overprocessed. The background is a 
smooth, neutral gradient that provides separation without distraction.

Post-processing includes subtle skin retouching that maintains natural texture 
while removing temporary blemishes, color correction for accurate representation, 
and contrast optimization that enhances depth. The final image has the quality 
of a high-end editorial portrait suitable for magazine covers or luxury brand 
campaigns.

Style & Atmosphere: The image embodies sun-kissed luxury with a timeless, 
editorial quality. The overall mood is sophisticated and confident, conveying 
professionalism while maintaining approachability. The aesthetic is clean and 
modern with subtle luxury undertones. This is the definitive reference image - 
the most important of the three for maintaining consistency across all future 
generations.

Critical Requirements: This image must show photorealistic quality with natural 
skin texture - every pore, fine line, and natural imperfection should be visible. 
Hair must appear as individual strands with natural variation. Eyes must have 
realistic catchlights and depth. The image should look like it was captured by 
a master portrait photographer, not generated by AI. Facial features must be 
consistent and distinctive, creating a recognizable individual who maintains 
their appearance across all three reference images. No artificial smoothness, 
no plastic appearance, no exaggerated features - only authentic, natural beauty 
captured with technical excellence.
```
**Word count:** ~500+ words
**Detail level:** Cinema-grade

---

## Why Premium Prompts Matter for FLUX

FLUX.1 is designed to understand **natural language** and **detailed descriptions** better than any previous model:

### FLUX Advantages with Detailed Prompts:

1. **Better Facial Consistency**
   - Detailed physical descriptions help FLUX maintain the same face
   - Specific features (eye color, hair texture, face shape) are preserved
   - Results in more consistent reference images

2. **Superior Photorealism**
   - Camera specs (Sony A7R IV, 85mm lens) trigger photorealistic rendering
   - Technical details (f/2.0, ISO 100) guide image quality
   - Results in professional photography look

3. **Natural Skin Texture**
   - Explicit instructions about pores and imperfections
   - FLUX avoids the "plastic AI skin" look
   - Results in believable, realistic skin

4. **Professional Lighting**
   - Detailed lighting setups (Rembrandt, softbox) guide FLUX
   - Results in dimensional, flattering illumination
   - Better for IPAdapter consistency later

5. **Better Prompt Adherence**
   - More details = more control
   - FLUX follows complex instructions better than simple prompts
   - Results in exactly what you described

---

## Quick Start Guide

### Step 1: Install Required Components

```bash
# Install WAS Node Suite (for automation)
cd /workspace/runpod-slim/ComfyUI/custom_nodes
git clone https://github.com/WASasquatch/was-node-suite-comfyui.git
cd was-node-suite-comfyui
pip install -r requirements.txt

# Or use our script:
bash scripts/install_was_nodes.sh
```

### Step 2: Generate Premium Prompts

```bash
cd "/workspace/## Super Factory - Open Code ##"
python scripts/generate_premium_prompts.py
```

**Output:**
- `input/prompts_premium_front.txt` (21 prompts)
- `input/prompts_premium_angle.txt` (21 prompts)
- `input/prompts_premium_natural.txt` (21 prompts)
- `input/prompts_premium_index.txt` (character list)

### Step 3: Load Premium Workflow

1. Open ComfyUI
2. Load: `workflows/flux_premium_automated_generator.json`
3. Check that model path is set to: `flux1-dev-fp8.safetensors`

### Step 4: Generate Reference Images

1. Set "Character Selector" to `1` (for char_001 ISABELLA_REYES)
2. Click **Queue Prompt**
3. Wait ~90 seconds (3 images × 30 sec each)
4. Images save automatically as:
   - `char_001_face_01.png`
   - `char_001_face_02.png`
   - `char_001_face_03.png`

### Step 5: Generate All Characters

Change "Character Selector" from 1 to 21 and run for each, or use batch automation.

---

## File Reference

### Scripts
- `generate_premium_prompts.py` - Creates cinema-grade prompts
- `install_was_nodes.sh` - Installs WAS Node Suite

### Workflows
- `flux_premium_automated_generator.json` - Full automation with premium prompts
- `flux_automated_reference_generator.json` - Basic automation (if preferred)
- `flux_reference_generator.json` - Manual workflow

### Generated Prompt Files
- `input/prompts_premium_front.txt` - Front-facing portraits
- `input/prompts_premium_angle.txt` - Three-quarter angles
- `input/prompts_premium_natural.txt` - Natural expressions
- `input/prompts_premium_index.txt` - Character index

---

## Expected Results

With premium prompts + FLUX.1:

**Per Image:**
- Generation time: ~30 seconds (RTX 4090)
- Quality: Photorealistic 8K
- Skin texture: Natural with visible pores
- Lighting: Professional studio quality
- Consistency: High across all 3 images

**Per Character (3 images):**
- Total time: ~90 seconds
- Result: 3 consistent reference photos
- Quality: Magazine/editorial level

**All 21 Characters (63 images):**
- Total time: ~30-35 minutes
- Result: 63 premium reference images
- Ready for IPAdapter bulk generation

---

## Tips for Best Results

### 1. Test One Character First
- Start with char_001 (ISABELLA_REYES)
- Check that all 3 images look like the same person
- Verify quality meets your standards

### 2. Review Generated Images
Check for:
- ✅ Consistent facial features across all 3 poses
- ✅ Natural skin texture (not plastic/smooth)
- ✅ Good lighting and contrast
- ✅ Sharp focus on eyes
- ✅ Same person in all 3 images

### 3. Adjust If Needed
If images don't match expectations:
- Check FLUX model is loaded correctly
- Verify prompts are loading from files
- Try adjusting the seed for variety
- Review persona JSON for accuracy

### 4. Quality Control
Before moving to bulk generation:
- Visually inspect all 63 reference images
- Ensure facial consistency for each character
- Check that lighting is good on all images
- Verify file naming is correct

---

## Troubleshooting

### "WAS node not found"
```bash
# Install WAS Node Suite
cd /workspace/runpod-slim/ComfyUI/custom_nodes
git clone https://github.com/WASasquatch/was-node-suite-comfyui.git
cd was-node-suite-comfyui
pip install -r requirements.txt
# Restart ComfyUI
```

### "File not found" errors
```bash
# Generate prompt files
cd "/workspace/## Super Factory - Open Code ##"
python scripts/generate_premium_prompts.py

# Verify files exist
ls input/prompts_premium_*.txt
```

### "Model not found"
- Download FLUX model: `flux1-dev-fp8.safetensors` (~17GB)
- Place in: `/workspace/runpod-slim/ComfyUI/models/checkpoints/`

### Images look inconsistent
- Use FLUX.1 Dev (not Schnell) for best consistency
- Check that all 3 prompts loaded correctly
- Ensure character selector is set correctly

---

## Next Steps After References

Once you have all 63 premium reference images:

1. **Verify References:**
   ```bash
   ls input/reference_images/ | wc -l
   # Should show 63 files
   ```

2. **Organize by Character:**
   ```bash
   python scripts/organize_reference_images.py
   ```

3. **Start Bulk Generation:**
   - Use master workflow with IPAdapter
   - Reference images ensure consistency
   - Generate 800 images per character (16,800 total)

---

## Summary

**Premium Prompt System:**
- ✅ Cinema-grade detail (500+ words per prompt)
- ✅ Professional photography terminology
- ✅ Specific camera and lighting specs
- ✅ Optimized for FLUX.1 natural language understanding
- ✅ Automated workflow with WAS Node Suite
- ✅ High consistency across reference images
- ✅ Natural photorealistic skin texture

**Time Investment:**
- Setup: 5 minutes
- Prompt generation: Instant
- All 63 references: ~35 minutes
- **Result:** Professional-quality reference images ready for bulk generation

**Quality Assurance:**
- Detailed prompts = Better FLUX results
- Professional specs = Photorealistic output
- Automation = Consistent processing
- Premium system = Magazine-quality references

---

Ready to generate premium reference images? Start with Step 1 above!
