"""Persona data model with validation and convenient accessors."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class Persona:
    """Represents a single AI model character with all their attributes."""

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @classmethod
    def load(cls, filepath: str) -> "Persona":
        """Load a persona from a JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            return cls(json.load(f))

    @classmethod
    def load_all(cls, directory: str) -> List["Persona"]:
        """Load all persona files from a directory, sorted by character_id."""
        personas = []
        for path in sorted(Path(directory).glob("char_*.json")):
            try:
                personas.append(cls.load(str(path)))
            except Exception as e:
                print(f"Warning: Could not load {path.name}: {e}")
        return personas

    # Core identity
    @property
    def character_id(self) -> str:
        return self._data.get("character_id", "")

    @property
    def name(self) -> str:
        return self._data.get("name", "")

    @property
    def safe_name(self) -> str:
        return self.name.replace(" ", "_")

    @property
    def age(self) -> int:
        return self._data.get("age", 25)

    @property
    def ethnicity(self) -> str:
        return self._data.get("ethnicity", "")

    @property
    def nationality(self) -> str:
        return self._data.get("nationality", "")

    @property
    def location(self) -> str:
        return self._data.get("location", "")

    @property
    def niche(self) -> str:
        return self._data.get("niche", "")

    # Physical description
    @property
    def physical(self) -> Dict[str, Any]:
        return self._data.get("physical_description", {})

    @property
    def height(self) -> str:
        return self.physical.get("height", "5'6\"")

    @property
    def body_type(self) -> str:
        return self.physical.get("body_type", "average")

    @property
    def build(self) -> str:
        return self.physical.get("build", self.body_type)

    @property
    def skin_tone(self) -> str:
        return self.physical.get("skin_tone", "natural")

    @property
    def hair_color(self) -> str:
        return self.physical.get("hair", {}).get("color", "brown")

    @property
    def hair_length(self) -> str:
        return self.physical.get("hair", {}).get("length", "medium")

    @property
    def hair_texture(self) -> str:
        return self.physical.get("hair", {}).get("texture", "straight")

    @property
    def eye_color(self) -> str:
        return self.physical.get("eyes", {}).get("color", "brown")

    @property
    def eye_shape(self) -> str:
        return self.physical.get("eyes", {}).get("shape", "almond")

    @property
    def face_shape(self) -> str:
        return self.physical.get("face_shape", "oval")

    @property
    def distinctive_features(self) -> str:
        return self.physical.get("distinctive_features", "")

    # Style
    @property
    def aesthetic(self) -> str:
        return self._data.get("style_persona", {}).get("aesthetic", "modern sophistication")

    @property
    def fashion_sense(self) -> str:
        return self._data.get("style_persona", {}).get("fashion_sense", "elegant contemporary")

    @property
    def personality_summary(self) -> str:
        return self._data.get("personality_summary", "")

    @property
    def locations(self) -> List[str]:
        return self._data.get("locations", [])

    @property
    def wardrobe(self) -> List[str]:
        return self._data.get("wardrobe", [])

    @property
    def content_preferences(self) -> Dict[str, List[str]]:
        return self._data.get("content_preferences", {})

    # Reference images
    def reference_image_names(self) -> List[str]:
        """Get expected reference image filenames."""
        return [f"{self.character_id}_face_{i:02d}.png" for i in range(1, 4)]

    def check_references(self, ref_dir: Path) -> tuple:
        """Check which reference images exist. Returns (ready, missing_list)."""
        missing = []
        for name in self.reference_image_names():
            path = ref_dir / name
            if not path.exists() or path.stat().st_size < 10000:
                missing.append(name)
        return len(missing) == 0, missing

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._data)

    def __repr__(self) -> str:
        return f"Persona({self.character_id}: {self.name})"
