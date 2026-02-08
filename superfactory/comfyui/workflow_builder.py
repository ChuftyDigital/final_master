"""Dynamic ComfyUI workflow construction.

Builds API-format workflow dicts programmatically instead of maintaining
fragile JSON files. Each method adds nodes and wires them together.
"""

import random
from typing import Any, Dict, List, Optional, Tuple


class WorkflowBuilder:
    """Constructs ComfyUI API-format workflows programmatically.

    Usage (Z-Image / Lumina2 models):
        wb = WorkflowBuilder()
        wb.load_checkpoint("z_image_bf16.safetensors")
        wb.load_clip("qwen_3_4b_fp8_mixed.safetensors", "lumina2")
        wb.load_vae("ae.safetensors")
        wb.set_prompt("Professional portrait photograph of...")
        wb.set_empty_latent(1024, 1024)
        wb.sample(steps=28, cfg=1.0, sampler="dpmpp_2m", scheduler="simple")
        wb.decode()
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
        """Load a checkpoint model. Outputs: MODEL(0), CLIP(1), VAE(2).

        For FLUX models, CLIP and VAE will be None — call load_dual_clip()
        and load_vae() separately.
        """
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
        """Load a single text encoder (for Z-Image/Lumina models).

        Args:
            clip_name: Text encoder filename (e.g. qwen_3_4b_fp8_mixed.safetensors)
            clip_type: "lumina2" for Z-Image, "sd1" for SD1.5, etc.
        """
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

    def set_prompt(self, positive: str, negative: str = "") -> "WorkflowBuilder":
        """Set positive and negative text prompts."""
        clip_ref = self._ref(self._clip[0], self._clip[1])

        pos_id = self._add_node("CLIPTextEncode", {
            "text": positive,
            "clip": clip_ref,
        })
        self._positive = pos_id

        if negative:
            neg_id = self._add_node("CLIPTextEncode", {
                "text": negative,
                "clip": clip_ref,
            })
            self._negative = neg_id
        else:
            neg_id = self._add_node("CLIPTextEncode", {
                "text": "",
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


def build_reference_workflow(
    prompt: str,
    checkpoint: str = "z_image_bf16.safetensors",
    vae: str = "ae.safetensors",
    text_encoder: str = "qwen_3_4b_fp8_mixed.safetensors",
    width: int = 1024,
    height: int = 1024,
    steps: int = 28,
    cfg: float = 1.0,
    sampler: str = "dpmpp_2m",
    scheduler: str = "simple",
    seed: Optional[int] = None,
    filename_prefix: str = "reference",
    negative: str = "",
) -> Dict[str, Any]:
    """Build a Z-Image reference image generation workflow.

    Z-Image Base works best with:
    - CFG 1.0
    - 28 steps with dpmpp_2m + simple scheduler
    - NO negative prompts (empty string)
    - Rich natural-language prompts
    """
    wb = WorkflowBuilder()
    wb.load_checkpoint(checkpoint)
    wb.load_clip(text_encoder, "lumina2")
    wb.load_vae(vae)
    wb.set_prompt(prompt, negative)
    wb.set_empty_latent(width, height)
    wb.sample(steps=steps, cfg=cfg, sampler=sampler, scheduler=scheduler, seed=seed)
    wb.decode()
    wb.save(filename_prefix)
    return wb.build()


def build_bulk_workflow(
    prompt: str,
    checkpoint: str = "z_image_turbo_bf16.safetensors",
    vae: str = "ae.safetensors",
    text_encoder: str = "qwen_3_4b_fp8_mixed.safetensors",
    width: int = 1024,
    height: int = 1536,
    steps: int = 8,
    cfg: float = 1.0,
    sampler: str = "dpmpp_2m",
    scheduler: str = "simple",
    seed: Optional[int] = None,
    filename_prefix: str = "generated",
    negative: str = "",
) -> Dict[str, Any]:
    """Build a Z-Image Turbo bulk generation workflow.

    Z-Image Turbo works best with:
    - CFG 1.0 (or 0.0 for pure distillation)
    - NO negative prompts (empty string)
    - 8 steps with dpmpp_2m + simple scheduler
    - Rich natural-language prompts (not tag-based)
    """
    wb = WorkflowBuilder()
    wb.load_checkpoint(checkpoint)
    wb.load_clip(text_encoder, "lumina2")
    wb.load_vae(vae)
    wb.set_prompt(prompt, negative)
    wb.set_empty_latent(width, height)
    wb.sample(steps=steps, cfg=cfg, sampler=sampler, scheduler=scheduler, seed=seed)
    wb.decode()
    wb.save(filename_prefix)
    return wb.build()
