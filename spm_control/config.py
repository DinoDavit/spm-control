from pathlib import Path
import yaml

def find_project_root(start: Path | None = None) -> Path:
    """
    Walk upward from this file until we find the project root.
    Project root is identified by pyproject.toml.
    """
    if start is None:
        start = Path(__file__).resolve()

    for parent in [start, *start.parents]:
        if (parent / "pyproject.toml").exists():
            return parent

    raise FileNotFoundError("Could not find project root containing pyproject.toml.")


PROJECT_ROOT = find_project_root()
CONFIG_FILES = PROJECT_ROOT / "config_files"

HARDWARE_CONFIG = CONFIG_FILES / "hardware.yaml"
SCAN_CONFIG = CONFIG_FILES / "scan.yaml"

def load_stage_config(path= HARDWARE_CONFIG):
    with open(path, "r") as file:
        config = yaml.safe_load(file)
    return config["stage"]

def load_piezo_motion(path= HARDWARE_CONFIG):
    with open(path, "r") as file:
        config = yaml.safe_load(file)
    return config["piezo_scan_motion"]

def load_hydraharp(path= HARDWARE_CONFIG):
    with open(path, "r") as file:
        config = yaml.safe_load(file)
    return config["piezo_scan_motion"]

def load_sync_config(path= HARDWARE_CONFIG):
    with open(path, "r") as file:
        config = yaml.safe_load(file)
    return config["sync"]

def load_scan_settings(path = SCAN_CONFIG):
    with open(path, "r") as file:
        config = yaml.safe_load(file)
    return config["sync"]