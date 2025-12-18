import yaml
from pathlib import Path

# project_root/src/common/config_loader.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_config(name: str) -> dict:
    path = PROJECT_ROOT / Path("configs") / name
    with open(path, "r") as f:
        return yaml.safe_load(f)
