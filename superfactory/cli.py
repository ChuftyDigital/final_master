"""Unified CLI - single entry point for the entire Super Factory system.

Usage:
    python main.py status                      Check setup status
    python main.py install --comfyui-path ...  Install models & nodes
    python main.py references                  Generate reference images
    python main.py references --character 1    Generate for one character
    python main.py generate                    Generate all content
    python main.py generate --lanes sfw        Generate specific lanes
    python main.py generate --character 1      Generate for one character
    python main.py generate --count 5          Override image count (test)
    python main.py prompts                     Export prompts to text files
    python main.py workflow --character 1      Export ComfyUI workflow JSON
"""

import argparse
import sys

from superfactory.config import Config
from superfactory.utils.logger import setup_logger


def cmd_status(args, config):
    """Show system status and readiness."""
    from superfactory.models.persona import Persona

    logger = setup_logger(log_file=config._get_nested(("logging", "file")))

    # Load personas
    personas = Persona.load_all(str(config.path("personas")))
    ref_dir = config.path("reference_images")

    logger.info("=" * 70)
    logger.info("SUPER FACTORY ULTIMATE - STATUS")
    logger.info("=" * 70)
    logger.info(f"Config: {args.config}")
    logger.info(f"ComfyUI: {config.comfyui_url}")
    logger.info(f"Personas: {len(personas)}")
    logger.info(f"Lanes: {', '.join(config.all_lanes())}")
    logger.info("")

    # Test ComfyUI connection
    from superfactory.comfyui.client import ComfyUIClient

    client = ComfyUIClient(
        server=config.comfyui_server,
        protocol=config._get_nested(("comfyui", "protocol"), "http"),
        verify_ssl=config.verify_ssl,
    )
    connected = client.test_connection()
    logger.info(f"ComfyUI: {'CONNECTED' if connected else 'NOT AVAILABLE'}")
    logger.info("")

    # Character status
    logger.info("Characters:")
    ready_count = 0
    for p in personas:
        ready, missing = p.check_references(ref_dir)
        status = "READY" if ready else f"MISSING {len(missing)} refs"
        if ready:
            ready_count += 1
        logger.info(f"  {p.character_id}: {p.name:30s} [{status}]")

    logger.info(f"\nReady: {ready_count}/{len(personas)} characters")


def cmd_install(args, config):
    """Install models and custom nodes."""
    from superfactory.models.installer import ModelInstaller

    logger = setup_logger(log_file=config._get_nested(("logging", "file")))
    installer = ModelInstaller(args.comfyui_path)

    if args.status_only:
        installer.status()
    else:
        installer.install_all()


def cmd_references(args, config):
    """Generate reference images."""
    from superfactory.comfyui.client import ComfyUIClient
    from superfactory.generation.prompt_engine import PromptEngine
    from superfactory.generation.reference_generator import ReferenceGenerator
    from superfactory.models.persona import Persona

    logger = setup_logger(log_file=config._get_nested(("logging", "file")))

    client = ComfyUIClient(
        server=config.comfyui_server,
        protocol=config._get_nested(("comfyui", "protocol"), "http"),
        timeout=config.timeout,
        verify_ssl=config.verify_ssl,
        max_retries=config.max_retries,
    )

    if not client.test_connection():
        logger.error("Cannot connect to ComfyUI. Start it first.")
        sys.exit(1)

    prompts = PromptEngine(str(config.path("templates")))
    generator = ReferenceGenerator(config, client, prompts)
    personas = Persona.load_all(str(config.path("personas")))

    if not personas:
        logger.error("No personas found. Add JSON files to the personas/ directory.")
        sys.exit(1)

    if args.character:
        # Filter to specific character
        idx = args.character - 1
        if 0 <= idx < len(personas):
            personas = [personas[idx]]
        else:
            logger.error(f"Character {args.character} not found (1-{len(personas)})")
            sys.exit(1)

    generator.generate_all(
        personas,
        skip_existing=not args.force,
        start_from=args.start_from,
    )


def cmd_generate(args, config):
    """Generate bulk content."""
    from superfactory.comfyui.client import ComfyUIClient
    from superfactory.generation.batch_generator import BatchGenerator
    from superfactory.generation.prompt_engine import PromptEngine
    from superfactory.models.persona import Persona

    logger = setup_logger(log_file=config._get_nested(("logging", "file")))

    client = ComfyUIClient(
        server=config.comfyui_server,
        protocol=config._get_nested(("comfyui", "protocol"), "http"),
        timeout=config.timeout,
        verify_ssl=config.verify_ssl,
        max_retries=config.max_retries,
    )

    if not args.dry_run and not client.test_connection():
        logger.error("Cannot connect to ComfyUI. Start it first.")
        sys.exit(1)

    prompts = PromptEngine(str(config.path("templates")))
    generator = BatchGenerator(config, client, prompts)
    personas = Persona.load_all(str(config.path("personas")))

    if not personas:
        logger.error("No personas found.")
        sys.exit(1)

    if args.character:
        idx = args.character - 1
        if 0 <= idx < len(personas):
            personas = [personas[idx]]
        else:
            logger.error(f"Character {args.character} not found")
            sys.exit(1)

    lanes = args.lanes if args.lanes else None

    if args.dry_run:
        logger.info("DRY RUN - checking setup only")
        ref_dir = config.path("reference_images")
        for p in personas:
            ready, missing = p.check_references(ref_dir)
            status = "READY" if ready else f"MISSING: {missing}"
            logger.info(f"  {p.name}: {status}")
        return

    generator.generate_all(
        personas,
        lanes=lanes,
        start_from=args.start_from,
        count_override=args.count,
    )


def cmd_prompts(args, config):
    """Export prompts to text files for manual use."""
    from superfactory.generation.prompt_engine import PromptEngine
    from superfactory.models.persona import Persona

    logger = setup_logger(log_file=config._get_nested(("logging", "file")))

    prompts = PromptEngine(str(config.path("templates")))
    personas = Persona.load_all(str(config.path("personas")))
    output_dir = config.path("output") / "exported_prompts"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Export reference prompts
    for pose in ["front", "angle", "natural"]:
        lines = []
        for p in personas:
            lines.append(f"### {p.character_id} | {p.name} ###")
            lines.append(prompts.reference_prompt(p, pose))
            lines.append("=" * 70)
            lines.append("")

        path = output_dir / f"reference_prompts_{pose}.txt"
        path.write_text("\n".join(lines), encoding="utf-8")
        logger.info(f"Exported: {path}")

    # Export bulk prompts per lane
    for lane in config.all_lanes():
        lines = []
        for p in personas:
            lines.append(f"### {p.character_id} | {p.name} ###")
            for i in range(5):  # 5 sample prompts per character
                lines.append(f"[{i+1}] {prompts.bulk_prompt(p, lane, i)}")
                lines.append("")
            lines.append("=" * 70)
            lines.append("")

        path = output_dir / f"bulk_prompts_{lane}.txt"
        path.write_text("\n".join(lines), encoding="utf-8")
        logger.info(f"Exported: {path}")

    logger.info(f"\nAll prompts exported to: {output_dir}")


def cmd_workflow(args, config):
    """Export ComfyUI workflow JSON files."""
    from superfactory.comfyui.workflow_builder import build_reference_workflow, build_bulk_workflow
    from superfactory.generation.prompt_engine import PromptEngine
    from superfactory.models.persona import Persona

    import json

    logger = setup_logger(log_file=config._get_nested(("logging", "file")))

    prompts = PromptEngine(str(config.path("templates")))
    personas = Persona.load_all(str(config.path("personas")))
    output_dir = config.path("workflows")
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.character:
        idx = args.character - 1
        if 0 <= idx < len(personas):
            personas = [personas[idx]]

    for p in personas:
        # Reference workflow
        for i, pose in enumerate(["front", "angle", "natural"], 1):
            prompt = prompts.reference_prompt(p, pose)
            wf = build_reference_workflow(
                prompt=prompt,
                checkpoint=config.model("reference_checkpoint", "flux1-dev-fp8.safetensors"),
                vae=config.model("vae", "ae.safetensors"),
                text_encoder_t5=config.model("text_encoder_t5", "t5xxl_fp8_e4m3fn.safetensors"),
                text_encoder_clip=config.model("text_encoder_clip", "clip_l.safetensors"),
                clip_type=config.model("clip_type", "flux"),
                filename_prefix=f"{p.character_id}_face_{i:02d}",
            )
            path = output_dir / f"{p.character_id}_reference_{pose}.json"
            with open(path, "w") as f:
                json.dump(wf, f, indent=2)

        logger.info(f"Exported workflows for {p.name}")

    logger.info(f"Workflows saved to: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        prog="superfactory",
        description="Super Factory Ultimate - AI Model Character Generation System",
    )
    parser.add_argument(
        "--config", default="config.yaml", help="Path to config file"
    )

    subs = parser.add_subparsers(dest="command", help="Command to run")

    # status
    p_status = subs.add_parser("status", help="Check system status")

    # install
    p_install = subs.add_parser("install", help="Install models and custom nodes")
    p_install.add_argument("--comfyui-path", default="/workspace/runpod-slim/ComfyUI", help="ComfyUI path")
    p_install.add_argument("--status-only", action="store_true", help="Show status only")

    # references
    p_refs = subs.add_parser("references", help="Generate reference images")
    p_refs.add_argument("--character", type=int, help="Character number (1-indexed)")
    p_refs.add_argument("--force", action="store_true", help="Regenerate existing")
    p_refs.add_argument("--start-from", type=int, default=0, help="Start from index")

    # generate
    p_gen = subs.add_parser("generate", help="Generate bulk content")
    p_gen.add_argument("--character", type=int, help="Character number (1-indexed)")
    p_gen.add_argument("--lanes", nargs="+", choices=["sfw", "suggestive", "spicy", "nsfw"])
    p_gen.add_argument("--count", type=int, help="Override image count per lane")
    p_gen.add_argument("--start-from", type=int, default=0, help="Start from index")
    p_gen.add_argument("--dry-run", action="store_true", help="Check setup only")

    # prompts
    p_prompts = subs.add_parser("prompts", help="Export prompts to text files")

    # workflow
    p_wf = subs.add_parser("workflow", help="Export ComfyUI workflow JSON")
    p_wf.add_argument("--character", type=int, help="Character number (1-indexed)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    config = Config.get(args.config)

    commands = {
        "status": cmd_status,
        "install": cmd_install,
        "references": cmd_references,
        "generate": cmd_generate,
        "prompts": cmd_prompts,
        "workflow": cmd_workflow,
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(args, config)
    else:
        parser.print_help()
