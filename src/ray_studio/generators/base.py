from abc import ABC, abstractmethod
from typing import Optional, Tuple
from ..dna.schema import BrandDNA

class GeneratorBase(ABC):
    """Base class for image generators."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        size: Tuple[int, int] = (1024, 1024),
        model: str = "flux/schnell",
        seed: Optional[int] = None
    ) -> bytes:
        """Generate image from prompt."""
        pass

    @abstractmethod
    async def generate_with_style(
        self,
        prompt: str,
        style: str,
        dna: BrandDNA,
        size: Tuple[int, int]
    ) -> bytes:
        """Generate with brand style applied."""
        pass
