import os
import yaml
from pathlib import Path
from typing import List
from .base import Template

TEMPLATE_DIR = Path("templates")

def list_templates() -> List[Template]:
    """List all available templates."""
    templates = []
    if not TEMPLATE_DIR.exists():
        return []

    for file in TEMPLATE_DIR.glob("*.yaml"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                templates.append(Template(**data))
        except Exception as e:
            print(f"Error loading template {file}: {e}")
            continue
    return templates

def get_template(name: str) -> Template:
    """Get a template by name."""
    file_path = TEMPLATE_DIR / f"{name}.yaml"
    if not file_path.exists():
        raise FileNotFoundError(f"Template not found: {name}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return Template(**data)
