from pathlib import Path
from typing import Any

import yaml

from .tree import ConfigTree


def _load_yaml(path: Path) -> dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def _load_dir(dir_path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {}

    if not dir_path.exists():
        return result

    for item in sorted(dir_path.iterdir()):
        if item.is_file() and item.suffix in (".yml", ".yaml"):
            content = _load_yaml(item)
            if item.stem in ("config", "base", "default"):
                result = _merge_dicts(result, content)
            else:
                if item.stem in result and isinstance(result[item.stem], dict):
                    result[item.stem] = _merge_dicts(result[item.stem], content)
                else:
                    result[item.stem] = content

        elif item.is_dir() and not item.name.startswith("."):
            sub_content = _load_dir(item)
            if item.name in result and isinstance(result[item.name], dict):
                result[item.name] = _merge_dicts(result[item.name], sub_content)
            else:
                result[item.name] = sub_content

    return result


def load_configs(config_dir: str | Path = "configs") -> ConfigTree:
    config_path = Path(config_dir)
    data = _load_dir(config_path)
    return ConfigTree(data)
