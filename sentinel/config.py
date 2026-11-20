"""Load Sentinel's YAML configuration."""

from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML configuration file and require a mapping at its root.

    Args:
        path: Path to the YAML configuration file.

    Raises:
        ValueError: If the YAML document is not a mapping.
        yaml.YAMLError: If the file contains invalid YAML.
        OSError: If the file cannot be read.
    """
    with Path(path).open("r", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    if not isinstance(config, dict):
        raise ValueError("The root of the Sentinel configuration must be a mapping.")

    return config
