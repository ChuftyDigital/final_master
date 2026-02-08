# ComfyUI Prompt Automation Guide

## Problem: API Automation Not Working
The Python scripts that try to automate ComfyUI via API were returning **400 Bad Request errors**. This is a common issue with ComfyUI's API authentication and workflow validation.

## Solution: Native ComfyUI Automation

We've created **two approaches** that work entirely within ComfyUI without API calls:

---

## 🚀 OPTION 1: AUTOMATED WORKFLOW (Recommended)

Uses **WAS Node Suite** custom nodes to load prompts from files automatically.

### Step 1: Install WAS Node Suite

```bash
cd /workspace/runpod-slim/ComfyUI/custom_nodes
git clone https://github.com/WASasquatch/was-node-suite-comfyui.git
cd was-node-suite-comfyui
pip install -r requirements.txt
```

Or run our script:
```bash
bash scripts/install_was_nodes.sh
```

### Step 2: Generate Batch Prompt Files

```bash
cd "/workspace/## Super Factory - Open Code ##"
python scripts/generate_batch_prompts.py
```

This creates:
- `input/prompts_batch_front.txt` - All 21 front-facing prompts
- `input/prompts_batch_angle.txt` - All 21 angle prompts  
- `input/prompts_batch_natural.txt` - All 21 natural prompts
- `input/prompts_index.txt` - Character list

### Step 3: Load Automated Workflow

1. In ComfyUI, load: `workflows/flux_automated_reference_generator.json`
2. The workflow has:
   - **Text Load From File** nodes (loads prompts automatically)
   - **Number Counter** node (selects which character to generate)
   - **Text Concatenate** nodes (builds filenames automatically)

### Step 4: Generate Images

1. Set the "Character Selector" node to the character number (1-21)
   - Or set to 0 to cycle through all automatically
2. Click **Queue Prompt**
3. The workflow will:
   - Load the correct prompt from the batch file
   - Generate all 3 images (front, angle, natural)
   - Save with correct naming: `char_XXX_face_01.png` etc.

**Time per character:** ~90 seconds (3 images × 30 sec with FLUX)

---

## 📝 OPTION 2: MANUAL WORKFLOW (Simpler)

If you don't want to install extra nodes, use the manual approach.

### Step 1: Generate Prompt Files

```bash
python scripts/generate_prompts_manual.py
```

This creates detailed .txt files in `generated_prompts/` folder.

### Step 2: Use Manual Workflow

1. Load: `workflows/flux_reference_generator.json`
2. Open `generated_prompts/char_001_ISABELLA_REYES_prompts.txt`
3. Copy the "IMAGE 01" prompt
4. Paste into "Prompt 1 (Front)" node in ComfyUI
5. Repeat for Prompt 2 and 3
6. Click Queue Prompt
7. Rename saved images to proper format

---

## 🔧 Troubleshooting

### "WAS node not found"
- Install WAS Node Suite (Option 1, Step 1)
- Restart ComfyUI completely

### "File not found" errors
- Make sure to run `generate_batch_prompts.py` first
- Check that `input/prompts_batch_*.txt` files exist

### Images not saving with correct names
- The automated workflow should handle this
- For manual: rename files to format: `char_001_face_01.png`

### Workflow validation errors
- Make sure FLUX model is downloaded: `flux1-dev-fp8.safetensors`
- Check model path in Checkpoint Loader node

---

## 📊 Comparison

| Feature | Option 1 (Automated) | Option 2 (Manual) |
|---------|---------------------|-------------------|
| Setup | Install WAS nodes | None needed |
| Speed | Fast - one click | Slower - copy-paste |
| Accuracy | High - automated naming | Manual renaming needed |
| Batch Processing | Yes | No |
| Best For | All 63 images | Testing 1-2 characters |

---

## 🎯 Quick Start Recommendation

**For generating all 63 reference images:**
1. Install WAS Node Suite (5 minutes)
2. Run `generate_batch_prompts.py`
3. Use automated workflow
4. Set Character Selector from 1 to 21
5. Done in ~30 minutes total

**For testing one character:**
1. Run `generate_prompts_manual.py`
2. Use manual workflow
3. Copy-paste prompts
4. Test with char_001 first

---

## 📁 File Reference

**Workflows:**
- `flux_automated_reference_generator.json` - Full automation with WAS nodes
- `flux_reference_generator.json` - Manual copy-paste version

**Scripts:**
- `generate_batch_prompts.py` - Creates batch files for automation
- `generate_prompts_manual.py` - Creates detailed individual files
- `install_was_nodes.sh` - Installs WAS Node Suite

**Generated Files:**
- `input/prompts_batch_*.txt` - Batch prompt files (for automation)
- `generated_prompts/*.txt` - Individual character files (for manual)

---

## ✅ Next Steps

1. Choose your option (Automated recommended)
2. Install/generate required files
3. Generate all 63 reference images
4. Move to bulk generation with IPAdapter

**Questions?** Check the workflow instructions node in ComfyUI for detailed steps.
