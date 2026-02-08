"""Unified configuration management. Loads config.yaml and allows CLI/env overrides."""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Single source of truth for all project configuration."""

    _instance = None
    _data: Dict[str, Any] = {}

    def __init__(self, config_path: Optional[str] = None):
        if config_path:
            self.load(config_path)

    @classmethod
    def get(cls, config_path: Optional[str] = None) -> "Config":
        """Get or create the singleton config instance."""
        if cls._instance is None:
            cls._instance = cls(config_path)
        return cls._instance

    def load(self, config_path: str):
        """Load configuration from YAML file."""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(path, "r") as f:
            self._data = yaml.safe_load(f)
        self._base_dir = path.parent
        self._apply_env_overrides()

    def _apply_env_overrides(self):
        """Allow environment variables to override config values."""
        env_map = {
            "COMFYUI_SERVER": ("comfyui", "server"),
            "COMFYUI_PROTOCOL": ("comfyui", "protocol"),
            "SF_OUTPUT_DIR": ("paths", "output"),
            "SF_LOG_LEVEL": ("logging", "level"),
        }
        for env_key, path in env_map.items():
            val = os.environ.get(env_key)
            if val:
                self._set_nested(path, val)

    def _set_nested(self, keys: tuple, value: Any):
        """Set a nested config value."""
        d = self._data
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = value

    def _get_nested(self, keys: tuple, default: Any = None) -> Any:
        """Get a nested config value."""
        d = self._data
        for key in keys:
            if isinstance(d, dict):
                d = d.get(key)
                if d is None:
                    return default
            else:
                return default
        return d

    @property
    def base_dir(self) -> Path:
        return self._base_dir

    @property
    def comfyui_server(self) -> str:
        return self._get_nested(("comfyui", "server"), "127.0.0.1:8188")

    @property
    def comfyui_url(self) -> str:
        proto = self._get_nested(("comfyui", "protocol"), "http")
        return f"{proto}://{self.comfyui_server}"

    @property
    def comfyui_ws_url(self) -> str:
        proto = "wss" if self._get_nested(("comfyui", "protocol")) == "https" else "ws"
        return f"{proto}://{self.comfyui_server}/ws"

    @property
    def timeout(self) -> int:
        return self._get_nested(("comfyui", "timeout"), 300)

    @property
    def verify_ssl(self) -> bool:
        return self._get_nested(("comfyui", "verify_ssl"), False)

    @property
    def max_retries(self) -> int:
        return self._get_nested(("comfyui", "max_retries"), 3)

    def path(self, key: str) -> Path:
        """Resolve a path relative to base_dir."""
        rel = self._get_nested(("paths", key), key)
        return self._base_dir / rel

    def generation(self, section: str, key: str, default: Any = None) -> Any:
        """Get a generation config value."""
        return self._get_nested(("generation", section, key), default)

    def model(self, key: str) -> str:
        """Get a model filename."""
        return self._get_nested(("models", key), "")

    def lane_config(self, lane: str) -> Dict[str, Any]:
        """Get lane-specific configuration."""
        return self._get_nested(("generation", "lanes", lane), {})

    def ipadapter_weights(self) -> list:
        """Get IPAdapter weights."""
        return self._get_nested(("generation", "ipadapter", "weights"), [0.7, 0.5, 0.4])

    def all_lanes(self) -> list:
        """Get all configured lane names."""
        lanes = self._get_nested(("generation", "lanes"), {})
        return list(lanes.keys())
