"""Dynamic ComfyUI workflow construction.

Builds API-format workflow dicts programmatically instead of maintaining
fragile JSON files. Each method adds nodes and wires them together.
"""

import random
from typing import Any, Dict, List, Optional, Tuple


class WorkflowBuilder:
    """Constructs ComfyUI API-format workflows programmatically.

    Usage:
        wb = WorkflowBuilder()
        wb.load_checkpoint("z_image_bf16.safetensors")
        wb.set_prompt("A portrait of...")
        wb.set_empty_latent(1024, 1024)
        wb.sample(steps=12, cfg=1.0)
        wb.decode()
        wb.save("output_prefix")
        workflow = wb.build()
    """

    def __init__(self):
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._next_id = 1
        # Track current pipeline state for chaining
        self._model: Optional[str] = None
        self._clip: Optional[str] = None
        self._vae: Optional[str] = None
        self._positive: Optional[str] = None
        self._negative: Optional[str] = None
        self._latent: Optional[str] = None
        self._image: Optional[str] = None

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
        self._model = nid
        self._clip = nid
        self._vae = nid
        return self

    def load_vae(self, vae_name: str) -> "WorkflowBuilder":
        """Load a separate VAE."""
        nid = self._add_node("VAELoader", {"vae_name": vae_name})
        self._vae = nid
        return self

    def set_prompt(self, positive: str, negative: str = "") -> "WorkflowBuilder":
        """Set positive and negative text prompts."""
        pos_id = self._add_node("CLIPTextEncode", {
            "text": positive,
            "clip": self._ref(self._clip, 1),
        })
        self._positive = pos_id

        if negative:
            neg_id = self._add_node("CLIPTextEncode", {
                "text": negative,
                "clip": self._ref(self._clip, 1),
            })
            self._negative = neg_id
        else:
            # Empty conditioning for models that don't use negative prompts
            neg_id = self._add_node("CLIPTextEncode", {
                "text": "",
                "clip": self._ref(self._clip, 1),
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
        steps: int = 12,
        cfg: float = 1.0,
        sampler: str = "dpmpp_2m",
        scheduler: str = "beta",
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
            "model": self._ref(self._model, 0),
            "positive": self._ref(self._positive, 0),
            "negative": self._ref(self._negative, 0),
            "latent_image": self._ref(self._latent, 0),
        })
        self._latent = nid
        return self

    def decode(self) -> "WorkflowBuilder":
        """Decode latent to image via VAE."""
        vae_output = 0 if self._nodes[self._vae]["class_type"] == "VAELoader" else 2
        nid = self._add_node("VAEDecode", {
            "samples": self._ref(self._latent, 0),
            "vae": self._ref(self._vae, vae_output),
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

    def load_ipadapter(self, model_name: str) -> str:
        """Load an IPAdapter model. Returns node ID."""
        return self._add_node("IPAdapterModelLoader", {"ipadapter_file": model_name})

    def load_clip_vision(self, model_name: str) -> str:
        """Load CLIP Vision model. Returns node ID."""
        return self._add_node("CLIPVisionLoader", {"clip_name": model_name})

    def apply_ipadapter(
        self,
        ipadapter_id: str,
        clip_vision_id: str,
        image_id: str,
        weight: float = 0.7,
        noise: float = 0.3,
        weight_type: str = "original",
        combine: str = "mean",
    ) -> "WorkflowBuilder":
        """Apply IPAdapter to the current model for face consistency."""
        nid = self._add_node("IPAdapterAdvanced", {
            "model": self._ref(self._model, 0),
            "ipadapter": self._ref(ipadapter_id, 0),
            "image": self._ref(image_id, 0),
            "clip_vision": self._ref(clip_vision_id, 0),
            "weight": weight,
            "noise": noise,
            "start_at": 0.0,
            "end_at": 1.0,
            "weight_type": weight_type,
            "combine_embeds": combine,
        })
        # IPAdapter outputs a modified MODEL at index 0
        self._model = nid
        return self

    def build(self) -> Dict[str, Dict[str, Any]]:
        """Return the complete workflow dict ready for the ComfyUI API."""
        return dict(self._nodes)


def build_reference_workflow(
    prompt: str,
    checkpoint: str = "z_image_bf16.safetensors",
    vae: str = "ae.safetensors",
    width: int = 1024,
    height: int = 1024,
    steps: int = 12,
    cfg: float = 1.0,
    sampler: str = "dpmpp_2m",
    scheduler: str = "beta",
    seed: Optional[int] = None,
    filename_prefix: str = "reference",
    negative: str = "blurry, low quality, cartoon, anime, distorted face, bad anatomy",
) -> Dict[str, Any]:
    """Build a simple reference image generation workflow."""
    wb = WorkflowBuilder()
    wb.load_checkpoint(checkpoint)
    wb.load_vae(vae)
    wb.set_prompt(prompt, negative)
    wb.set_empty_latent(width, height)
    wb.sample(steps=steps, cfg=cfg, sampler=sampler, scheduler=scheduler, seed=seed)
    wb.decode()
    wb.save(filename_prefix)
    return wb.build()


def build_bulk_workflow(
    prompt: str,
    reference_images: List[str],
    checkpoint: str = "z_image_turbo_bf16.safetensors",
    vae: str = "ae.safetensors",
    ipadapter_model: str = "ip-adapter-plus_sd15.bin",
    clip_vision_model: str = "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors",
    ipadapter_weights: List[float] = None,
    width: int = 1024,
    height: int = 1536,
    steps: int = 8,
    cfg: float = 1.0,
    sampler: str = "dpmpp_2m",
    scheduler: str = "beta",
    seed: Optional[int] = None,
    filename_prefix: str = "generated",
    negative: str = "blurry, low quality, distorted, bad anatomy, inconsistent face",
) -> Dict[str, Any]:
    """Build a bulk generation workflow with IPAdapter face consistency."""
    if ipadapter_weights is None:
        ipadapter_weights = [0.7, 0.5, 0.4]

    wb = WorkflowBuilder()
    wb.load_checkpoint(checkpoint)
    wb.load_vae(vae)

    # Load IPAdapter and CLIP Vision
    ipa_id = wb.load_ipadapter(ipadapter_model)
    clip_v_id = wb.load_clip_vision(clip_vision_model)

    # Apply each reference image with decreasing weight
    for i, ref_img in enumerate(reference_images):
        weight = ipadapter_weights[i] if i < len(ipadapter_weights) else 0.3
        img_id = wb.load_image(ref_img)
        wb.apply_ipadapter(ipa_id, clip_v_id, img_id, weight=weight)

    wb.set_prompt(prompt, negative)
    wb.set_empty_latent(width, height)
    wb.sample(steps=steps, cfg=cfg, sampler=sampler, scheduler=scheduler, seed=seed)
    wb.decode()
    wb.save(filename_prefix)
    return wb.build()
