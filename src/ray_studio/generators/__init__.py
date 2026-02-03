import os
from .base import GeneratorBase
from .fal import FalGenerator

def get_generator() -> GeneratorBase:
    """Get the configured generator."""
    # Default to Fal for now
    api_key = os.getenv("FAL_API_KEY")
    return FalGenerator(api_key=api_key)

__all__ = ["GeneratorBase", "FalGenerator", "get_generator"]
