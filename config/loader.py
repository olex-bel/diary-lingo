import tomllib
import re
from typing import Any
from pathlib import Path
from copy import deepcopy

SUPPORTED_LLM_PROVIDERS = {'ollama'}
DEFAULT_CONFIG: dict[str, Any] = {
    "app": {
        "window_geometry": "400x400",
        "font_family": "Arial",
        "font_size_main": 12,
        "font_size_ui": 10,
    },
    "llm": {
        "provider": "",
        "model": "",
        "temperature": 0.7,
    },
    "translator": {
        "provider": "",
        "model": "",
        "temperature": 0.7,
    },
}

def merge_configs(default: dict[str, Any], user: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(default)

    for key, value in user.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = merge_configs(result[key], value) # type: ignore
        else:
            result[key] = value

    return result

def validate_config(cfg: dict[str, Any]) -> None:
    llm = cfg["llm"]

    if not isinstance(llm["temperature"], (int, float)):
        raise TypeError("llm.temperature must be a number")

    if llm["provider"] not in SUPPORTED_LLM_PROVIDERS:
        raise ValueError(f"llm.provider must be one of {SUPPORTED_LLM_PROVIDERS}")

    if not (0.0 <= llm["temperature"] <= 2.0):
        raise ValueError("llm.temperature must be between 0.0 and 2.0")

    if not isinstance(cfg["app"]["window_geometry"], str):
        raise TypeError("app.window_geometry must be a string")
    
    if not re.match(r'^\d+x\d+$', cfg["app"]["window_geometry"]):
        raise ValueError("app.window_geometry must be in the format WIDTHxHEIGHT, e.g., 800x600")
    
    if not isinstance(cfg["app"]["font_size_main"], int) or not isinstance(cfg["app"]["font_size_ui"], int):
        raise TypeError("app.font_size_main and app.font_size_ui must be integers")

def load_config(path: str | Path) -> dict[str, Any]:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f'Config file not found: {path}')

    with open(path, 'rb') as f:
        config = tomllib.load(f)
        config = merge_configs(DEFAULT_CONFIG, config)
        validate_config(config)
        return config
    