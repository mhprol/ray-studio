import json
import os
from typing import Dict, Any, Optional
from pydantic import BaseModel, ConfigDict

class Brand(BaseModel):
    instagramHandle: Optional[str] = None
    primaryColor: Optional[str] = None
    secondaryColor: Optional[str] = None
    model_config = ConfigDict(extra="allow")

class FigmaProject(BaseModel):
    name: str = "New Project"
    fileId: str = ""
    brand: Brand = Brand()
    templates: Dict[str, Any] = {}
    model_config = ConfigDict(extra="allow")

class FigmaConfig:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or self._find_config()
        self.project: Optional[FigmaProject] = None
        if self.config_path:
            try:
                self.load()
            except FileNotFoundError:
                # If explicitly provided path doesn't exist, we might want to just set project to default
                # or handle it in load. Here we let __init__ complete, load will be retried or user handles it.
                pass

    def _find_config(self) -> Optional[str]:
        # Search paths: ./Ray/figma-project.json, ./figma-project.json
        candidates = [
            os.path.join(os.getcwd(), "Ray", "figma-project.json"),
            os.path.join(os.getcwd(), "figma-project.json"),
        ]
        for p in candidates:
            if os.path.exists(p):
                return p
        return None

    def load(self):
        if not self.config_path:
            return

        if not os.path.exists(self.config_path):
             raise FileNotFoundError(f"Config file not found at {self.config_path}")

        with open(self.config_path, "r") as f:
            data = json.load(f)
            self.project = FigmaProject(**data)

    def get_node_id(self, template_path: str) -> Optional[str]:
        """
        Resolve a dot-notation path to a node ID.
        Example: 'socialMedia.postPreview1.headline'
        Supports both direct nesting and 'children' nesting.
        """
        if not self.project:
            return None

        parts = template_path.split(".")
        if not parts:
            return None

        current = self.project.templates

        # Initial lookup in root templates dict
        first = parts.pop(0)
        if first in current:
            current = current[first]
        else:
            return None

        for part in parts:
            if not isinstance(current, dict):
                return None

            # Try to find part in current dict
            found = False

            # 1. Direct key
            if part in current:
                current = current[part]
                found = True

            # 2. Inside 'children'
            elif "children" in current and isinstance(current["children"], dict) and part in current["children"]:
                current = current["children"][part]
                found = True

            if not found:
                return None

        # If we reached here, current is the target node object
        if isinstance(current, dict) and "nodeId" in current:
            return current["nodeId"]

        return None

    def save(self):
        """Save the current configuration back to the file."""
        if not self.config_path:
             raise ValueError("No config path set")

        # Ensure dir exists
        os.makedirs(os.path.dirname(os.path.abspath(self.config_path)), exist_ok=True)

        with open(self.config_path, "w") as f:
            if self.project:
                json.dump(self.project.model_dump(), f, indent=2)

    @classmethod
    def create_template(cls, path: str, name: str):
        """Create a default template config file."""
        project = FigmaProject(name=name)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w") as f:
            json.dump(project.model_dump(), f, indent=2)
