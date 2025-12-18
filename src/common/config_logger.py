import yaml
from pathlib import Path


def load_config(name: str) -> dict:
    path = Path("config") / name
    with open(path, "r") as f:
        return yaml.safe_load(f)
