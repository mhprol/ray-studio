import httpx
import os
from typing import Tuple, Optional
from .base import GeneratorBase
from ..dna.schema import BrandDNA

class FalGenerator(GeneratorBase):
    """fal.ai Flux image generation"""

    BASE_URL = "https://fal.run/fal-ai"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("FAL_API_KEY")
        if not self.api_key:
            # We don't raise error here to allow instantiating for testing/mocking,
            # but it will fail on generate if not provided.
            pass

    async def generate(
        self,
        prompt: str,
        size: Tuple[int, int] = (1024, 1024),
        model: str = "flux/schnell",  # schnell (fast) or dev (quality)
        seed: Optional[int] = None
    ) -> bytes:
        """Generate image from prompt"""

        if not self.api_key:
            raise ValueError("FAL_API_KEY is not set")

        async with httpx.AsyncClient(headers={"Authorization": f"Key {self.api_key}"}) as client:
            response = await client.post(
                f"{self.BASE_URL}/{model}",
                json={
                    "prompt": prompt,
                    "image_size": {"width": size[0], "height": size[1]},
                    "seed": seed,
                    "num_images": 1
                },
                timeout=60.0
            )

            response.raise_for_status()
            result = response.json()
            image_url = result["images"][0]["url"]

            # Download image
            img_response = await client.get(image_url, timeout=30.0)
            img_response.raise_for_status()
            return img_response.content

    async def generate_with_style(
        self,
        prompt: str,
        style: str,  # elegante, vibrante, minimal, etc.
        dna: BrandDNA,
        size: Tuple[int, int]
    ) -> bytes:
        """Generate with brand style applied"""

        style_prompts = {
            "elegante": "elegant, sophisticated, premium, clean lines",
            "vibrante": "vibrant, colorful, energetic, dynamic",
            "minimal": "minimalist, clean, simple, whitespace",
            "bold": "bold, impactful, strong contrast, dramatic",
            "warm": "warm tones, cozy, inviting, soft lighting",
        }

        dna_style = style_prompts.get(style, "")
        if not dna_style:
             # Try to use dna.tone if style not found
             dna_style = dna.tone

        enhanced_prompt = f"{prompt}, {dna_style}, color palette: {dna.brand.colors.primary} and {dna.brand.colors.secondary}"

        return await self.generate(enhanced_prompt, size)
