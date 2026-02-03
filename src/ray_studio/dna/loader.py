import yaml
from pathlib import Path
from .schema import BrandDNA

def load_dna(path: str) -> BrandDNA:
    """Load Brand DNA from a YAML file."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"DNA file not found: {path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return BrandDNA(**data)
