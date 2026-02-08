#!/usr/bin/env python3
"""Super Factory Ultimate - Single entry point.

Usage:
    python main.py status                         Check system status
    python main.py install --comfyui-path /path   Install models & nodes
    python main.py references                     Generate reference images
    python main.py generate                       Generate all content
    python main.py generate --lanes sfw --count 5 Test with small batch
    python main.py prompts                        Export prompts to files
    python main.py workflow                       Export ComfyUI workflows
"""

from superfactory.cli import main

if __name__ == "__main__":
    main()
