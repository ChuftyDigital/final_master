"""Dynamic ComfyUI workflow construction.

Builds API-format workflow dicts programmatically instead of maintaining
fragile JSON files. Each method adds nodes and wires them together.

Photorealistic pipeline:
  Generate → FluxPromptEnhance → KSampler → VAEDecode
  → FaceDetailer (Impact Pack) → ColorMatch (KJNodes) → Upscale (4x-UltraSharp) → Save

Supports both FLUX and Z-Image/Lumina2 model pipelines.
"""

import random
from typing import Any, Dict, List, Optional, Tuple


class WorkflowBuilder:
    """Constructs ComfyUI API-format workflows programmatically.

    Usage (FLUX photorealistic pipeline):
        wb = WorkflowBuilder()
        wb.load_checkpoint("flux1-dev-fp8.safetensors")
        wb.load_dual_clip("t5xxl_fp8_e4m3fn.safetensors", "clip_l.safetensors", "flux")
        wb.load_vae("ae.safetensors")
        wb.set_prompt("Editorial portrait...", "blurry...", enhance=True)
        wb.set_empty_latent(1024, 1024)
        wb.sample(steps=28, cfg=1.0, sampler="euler", scheduler="normal")
        wb.decode()
        wb.face_detail()          # FaceDetailer pass for realistic faces
        wb.color_match(ref_id)    # Harmonize face lighting with original
        wb.upscale("4x-UltraSharp.pth")  # High-res upscale
        wb.save("output_prefix")
        workflow = wb.build()
    """

    def __init__(self):
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._next_id = 1
        # Track current pipeline state for chaining
        # Each stores (node_id, output_index)
        self._model: Optional[Tuple[str, int]] = None
        self._clip: Optional[Tuple[str, int]] = None
        self._vae: Optional[Tuple[str, int]] = None
        self._positive: Optional[str] = None
        self._negative: Optional[str] = None
        self._latent: Optional[str] = None
        self._image: Optional[str] = None
        # Face detection models (loaded on demand)
        self._bbox_detector: Optional[str] = None
        self._sam_model: Optional[str] = None

    def _add_node(self, class_type: str, inputs: Dict[str, Any]) -> str:
        """Add a node and return its ID string."""
        node_id = str(self._next_id)
        self._next_id += 1
        self._nodes[node_id] = {"class_type": class_type, "inputs": inputs}
        return node_id

    def _ref(self, node_id: str, output_idx: int = 0) -> List:
        """Create a node reference [node_id, output_index]."""
        return [node_id, output_idx]

    def load_checkpoint(self, ckpt_name: str) -> "WorkflowBuilder":
        """Load a checkpoint model. Outputs: MODEL(0), CLIP(1), VAE(2)."""
        nid = self._add_node("CheckpointLoaderSimple", {"ckpt_name": ckpt_name})
        self._model = (nid, 0)
        self._clip = (nid, 1)
        self._vae = (nid, 2)
        return self

    def load_dual_clip(
        self, clip_name1: str, clip_name2: str, clip_type: str = "flux"
    ) -> "WorkflowBuilder":
        """Load dual CLIP text encoders (for FLUX models).

        Args:
            clip_name1: T5-XXL encoder filename
            clip_name2: CLIP-L encoder filename
            clip_type: "flux" or "sdxl"
        """
        nid = self._add_node("DualCLIPLoader", {
            "clip_name1": clip_name1,
            "clip_name2": clip_name2,
            "type": clip_type,
        })
        self._clip = (nid, 0)
        return self

    def load_clip(self, clip_name: str, clip_type: str = "lumina2") -> "WorkflowBuilder":
        """Load a single text encoder (for Z-Image/Lumina models)."""
        nid = self._add_node("CLIPLoader", {
            "clip_name": clip_name,
            "type": clip_type,
        })
        self._clip = (nid, 0)
        return self

    def load_vae(self, vae_name: str) -> "WorkflowBuilder":
        """Load a separate VAE."""
        nid = self._add_node("VAELoader", {"vae_name": vae_name})
        self._vae = (nid, 0)
        return self

    def enhance_prompt(self, text: str, seed: Optional[int] = None) -> str:
        """Run prompt through FluxPromptEnhance node.

        Requires ComfyUI-Fluxpromptenhancer custom node installed.
        Returns the node ID whose output 0 is the enhanced STRING.
        """
        if seed is None:
            seed = random.randint(1, 2**31)
        nid = self._add_node("FluxPromptEnhance", {
            "prompt": text,
            "seed": seed,
        })
        return nid

    def set_prompt(
        self, positive: str, negative: str = "", enhance: bool = False, enhance_seed: Optional[int] = None,
    ) -> "WorkflowBuilder":
        """Set positive and negative text prompts.

        If enhance=True, the positive prompt is first run through
        FluxPromptEnhance before CLIP encoding.
        """
        clip_ref = self._ref(self._clip[0], self._clip[1])

        if enhance:
            enhancer_id = self.enhance_prompt(positive, seed=enhance_seed)
            pos_id = self._add_node("CLIPTextEncode", {
                "text": self._ref(enhancer_id, 0),
                "clip": clip_ref,
            })
        else:
            pos_id = self._add_node("CLIPTextEncode", {
                "text": positive,
                "clip": clip_ref,
            })
        self._positive = pos_id

        neg_id = self._add_node("CLIPTextEncode", {
            "text": negative if negative else "",
            "clip": clip_ref,
        })
        self._negative = neg_id

        return self

    def set_empty_latent(self, width: int = 1024, height: int = 1024, batch: int = 1) -> "WorkflowBuilder":
        """Create an empty latent image."""
        nid = self._add_node("EmptyLatentImage", {
            "width": width,
            "height": height,
            "batch_size": batch,
        })
        self._latent = nid
        return self

    def sample(
        self,
        steps: int = 28,
        cfg: float = 1.0,
        sampler: str = "euler",
        scheduler: str = "normal",
        seed: Optional[int] = None,
        denoise: float = 1.0,
    ) -> "WorkflowBuilder":
        """Run the KSampler."""
        if seed is None:
            seed = random.randint(1, 2**31)

        nid = self._add_node("KSampler", {
            "seed": seed,
            "steps": steps,
            "cfg": cfg,
            "sampler_name": sampler,
            "scheduler": scheduler,
            "denoise": denoise,
            "model": self._ref(self._model[0], self._model[1]),
            "positive": self._ref(self._positive, 0),
            "negative": self._ref(self._negative, 0),
            "latent_image": self._ref(self._latent, 0),
        })
        self._latent = nid
        return self

    def decode(self) -> "WorkflowBuilder":
        """Decode latent to image via VAE."""
        nid = self._add_node("VAEDecode", {
            "samples": self._ref(self._latent, 0),
            "vae": self._ref(self._vae[0], self._vae[1]),
        })
        self._image = nid
        return self

    # ── Face Detection & Detail ───────────────────────────────────

    def load_face_detector(self, model_name: str = "bbox/face_yolov8m.pt") -> "WorkflowBuilder":
        """Load YOLO face detector via UltralyticsDetectorProvider (Impact Pack)."""
        nid = self._add_node("UltralyticsDetectorProvider", {
            "model_name": model_name,
        })
        self._bbox_detector = nid
        return self

    def load_sam(self, model_name: str = "sam_vit_b_01ec64.pth", device: str = "AUTO") -> "WorkflowBuilder":
        """Load SAM segmentation model (Impact Pack)."""
        nid = self._add_node("SAMLoader", {
            "model_name": model_name,
            "device_mode": device,
        })
        self._sam_model = nid
        return self

    def face_detail(
        self,
        steps: int = 20,
        cfg: float = 1.0,
        sampler: str = "euler",
        scheduler: str = "normal",
        denoise: float = 0.35,
        guide_size: int = 512,
        max_size: int = 1024,
        seed: Optional[int] = None,
        bbox_threshold: float = 0.5,
        bbox_dilation: int = 10,
        bbox_crop_factor: float = 3.0,
        feather: int = 5,
    ) -> "WorkflowBuilder":
        """Run FaceDetailer to enhance face realism (Impact Pack).

        Detects faces, crops them, runs a second KSampler pass at higher
        detail, then composites back. Essential for photorealistic portraits.

        Args:
            denoise: How much to refine face (0.3-0.4 = faithful, 0.5+ = creative)
            guide_size: Face crop resolution for detail pass
        """
        if seed is None:
            seed = random.randint(1, 2**31)

        # Auto-load detector models if not already loaded
        if self._bbox_detector is None:
            self.load_face_detector()
        if self._sam_model is None:
            self.load_sam()

        nid = self._add_node("FaceDetailer", {
            "image": self._ref(self._image, 0),
            "model": self._ref(self._model[0], self._model[1]),
            "clip": self._ref(self._clip[0], self._clip[1]),
            "vae": self._ref(self._vae[0], self._vae[1]),
            "positive": self._ref(self._positive, 0),
            "negative": self._ref(self._negative, 0),
            "bbox_detector": self._ref(self._bbox_detector, 0),
            "sam_model_opt": self._ref(self._sam_model, 0),
            "guide_size": guide_size,
            "guide_size_for": True,
            "max_size": max_size,
            "seed": seed,
            "steps": steps,
            "cfg": cfg,
            "sampler_name": sampler,
            "scheduler": scheduler,
            "denoise": denoise,
            "feather": feather,
            "noise_mask": True,
            "force_inpaint": True,
            "bbox_threshold": bbox_threshold,
            "bbox_dilation": bbox_dilation,
            "bbox_crop_factor": bbox_crop_factor,
            "sam_detection_hint": "center-1",
            "sam_dilation": 0,
            "sam_threshold": 0.93,
            "sam_bbox_expansion": 0,
            "sam_mask_hint_threshold": 0.7,
            "sam_mask_hint_use_negative": "False",
            "drop_size": 10,
            "wildcard": "",
            "cycle": 1,
        })
        # FaceDetailer output 0 is the enhanced image
        self._image = nid
        return self

    # ── Color Harmonization ────────────────────────────────────────

    def color_match(
        self,
        reference_image_id: str,
        method: str = "mkl",
    ) -> "WorkflowBuilder":
        """Match color/lighting of current image to a reference image.

        Requires ComfyUI-KJNodes custom node. Prevents the "patched face"
        look after FaceDetailer by harmonizing color between the detailed
        face region and the overall image lighting.

        Args:
            reference_image_id: Node ID of the reference image to match colors from
            method: Color matching algorithm ("mkl", "hm", "reinhard")
        """
        nid = self._add_node("ColorMatch", {
            "image_ref": self._ref(reference_image_id, 0),
            "image_target": self._ref(self._image, 0),
            "method": method,
        })
        self._image = nid
        return self

    # ── Upscaling ─────────────────────────────────────────────────

    def upscale(self, model_name: str = "4x-UltraSharp.pth") -> "WorkflowBuilder":
        """Upscale image using a model (e.g. 4x-UltraSharp).

        Loads the upscale model and applies it to the current image.
        """
        loader_id = self._add_node("UpscaleModelLoader", {
            "model_name": model_name,
        })
        nid = self._add_node("ImageUpscaleWithModel", {
            "upscale_model": self._ref(loader_id, 0),
            "image": self._ref(self._image, 0),
        })
        self._image = nid
        return self

    def scale_to_pixels(self, megapixels: float = 4.0, method: str = "lanczos") -> "WorkflowBuilder":
        """Scale image to a target total megapixel count.

        Useful after 4x upscale to control final resolution.
        e.g. megapixels=4.0 → ~2048x2048 for square images.
        """
        nid = self._add_node("ImageScaleToTotalPixels", {
            "image": self._ref(self._image, 0),
            "upscale_method": method,
            "megapixels": megapixels,
            "resolution_steps": 8,
        })
        self._image = nid
        return self

    def save(self, filename_prefix: str = "superfactory") -> "WorkflowBuilder":
        """Save the current image."""
        self._add_node("SaveImage", {
            "filename_prefix": filename_prefix,
            "images": self._ref(self._image, 0),
        })
        return self

    def load_image(self, image_path: str) -> str:
        """Load an image from disk. Returns node ID."""
        nid = self._add_node("LoadImage", {"image": image_path})
        self._image = nid
        return nid

    def build(self) -> Dict[str, Dict[str, Any]]:
        """Return the complete workflow dict ready for the ComfyUI API."""
        return dict(self._nodes)


# ── FLUX workflow builders (primary pipeline) ──────────────────────


def build_reference_workflow(
    prompt: str,
    checkpoint: str = "flux1-dev-fp8.safetensors",
    vae: str = "ae.safetensors",
    text_encoder_t5: str = "t5xxl_fp8_e4m3fn.safetensors",
    text_encoder_clip: str = "clip_l.safetensors",
    clip_type: str = "flux",
    width: int = 1024,
    height: int = 1024,
    steps: int = 28,
    cfg: float = 1.0,
    sampler: str = "euler",
    scheduler: str = "normal",
    seed: Optional[int] = None,
    filename_prefix: str = "reference",
    negative: str = "blurry, low quality, cartoon, anime, distorted face, bad anatomy, deformed features, plastic skin, airbrushed skin, overly smooth skin, studio backdrop, grey background, neutral background, oversaturated, jpeg artifacts, watermark, text, logo, doll-like, mannequin, CGI, 3D render",
    enhance_prompt: bool = False,
    face_detail: bool = True,
    face_detail_denoise: float = 0.35,
    upscale_model: str = "4x-UltraSharp.pth",
    upscale: bool = True,
    upscale_megapixels: float = 4.0,
) -> Dict[str, Any]:
    """Build a FLUX photorealistic reference image workflow.

    Full pipeline: KSampler (euler/normal)
    → FaceDetailer (Impact Pack) → ColorMatch (KJNodes) → 4x-UltraSharp Upscale → Save

    FLUX.1 Dev with FP8 on RTX 5090:
    - 28 steps with euler + normal scheduler
    - CFG 1.0
    - FluxPromptEnhance for AI-enhanced prompts
    - FaceDetailer for realistic face refinement
    - 4x-UltraSharp upscale for maximum detail
    - ~60-90 seconds per image on RTX 5090
    """
    wb = WorkflowBuilder()
    wb.load_checkpoint(checkpoint)
    wb.load_dual_clip(text_encoder_t5, text_encoder_clip, clip_type)
    wb.load_vae(vae)
    wb.set_prompt(prompt, negative, enhance=enhance_prompt)
    wb.set_empty_latent(width, height)
    wb.sample(steps=steps, cfg=cfg, sampler=sampler, scheduler=scheduler, seed=seed)
    wb.decode()

    # FaceDetailer: detect face, crop, run second detail pass, composite back
    if face_detail:
        # Save pre-FaceDetailer image ref for ColorMatch harmonization
        pre_face_image = wb._image
        wb.face_detail(
            steps=20,
            cfg=cfg,
            sampler=sampler,
            scheduler=scheduler,
            denoise=face_detail_denoise,
        )
        # ColorMatch: harmonize face-detailed result with original lighting
        wb.color_match(reference_image_id=pre_face_image)

    # Upscale for maximum detail and skin texture
    if upscale:
        wb.upscale(upscale_model)
        wb.scale_to_pixels(megapixels=upscale_megapixels)

    wb.save(filename_prefix)
    return wb.build()


def build_bulk_workflow(
    prompt: str,
    checkpoint: str = "flux1-dev-fp8.safetensors",
    vae: str = "ae.safetensors",
    text_encoder_t5: str = "t5xxl_fp8_e4m3fn.safetensors",
    text_encoder_clip: str = "clip_l.safetensors",
    clip_type: str = "flux",
    width: int = 1024,
    height: int = 1536,
    steps: int = 28,
    cfg: float = 1.0,
    sampler: str = "euler",
    scheduler: str = "normal",
    seed: Optional[int] = None,
    filename_prefix: str = "generated",
    negative: str = "blurry, low quality, cartoon, anime, distorted face, bad anatomy, deformed features, plastic skin, airbrushed skin, overly smooth skin, studio backdrop, grey background, neutral background, oversaturated, jpeg artifacts, watermark, text, logo, doll-like, mannequin, CGI, 3D render",
    enhance_prompt: bool = False,
    face_detail: bool = True,
    face_detail_denoise: float = 0.35,
    upscale_model: str = "4x-UltraSharp.pth",
    upscale: bool = False,
    upscale_megapixels: float = 4.0,
) -> Dict[str, Any]:
    """Build a FLUX photorealistic bulk generation workflow.

    Same pipeline as reference. FaceDetailer enabled by default.
    Upscale disabled by default for bulk (speed), enable if needed.
    """
    wb = WorkflowBuilder()
    wb.load_checkpoint(checkpoint)
    wb.load_dual_clip(text_encoder_t5, text_encoder_clip, clip_type)
    wb.load_vae(vae)
    wb.set_prompt(prompt, negative, enhance=enhance_prompt)
    wb.set_empty_latent(width, height)
    wb.sample(steps=steps, cfg=cfg, sampler=sampler, scheduler=scheduler, seed=seed)
    wb.decode()

    if face_detail:
        pre_face_image = wb._image
        wb.face_detail(
            steps=20,
            cfg=cfg,
            sampler=sampler,
            scheduler=scheduler,
            denoise=face_detail_denoise,
        )
        wb.color_match(reference_image_id=pre_face_image)

    if upscale:
        wb.upscale(upscale_model)
        wb.scale_to_pixels(megapixels=upscale_megapixels)

    wb.save(filename_prefix)
    return wb.build()
