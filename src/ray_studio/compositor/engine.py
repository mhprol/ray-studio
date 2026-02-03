from PIL import Image
from typing import Dict, Any, Optional
from ..templates.base import Template
from ..dna.schema import BrandDNA
from ..generators.base import GeneratorBase
from .layers import LayerRenderer

class Compositor:
    """Core image composition engine."""

    def render(
        self,
        template: Template,
        dna: BrandDNA,
        inputs: Dict[str, Any],
        generator: Optional[GeneratorBase] = None,
        seed: Optional[int] = None
    ) -> Image.Image:
        """Render a template into an image."""

        # Determine canvas size
        # For now, default to 1080x1080 if not specified
        width = 1080
        height = 1080

        # Create base canvas
        canvas = Image.new("RGBA", (width, height), (255, 255, 255, 255))

        layer_renderer = LayerRenderer(dna)

        # Validate inputs against template
        # (Skipping robust validation for now)

        prev_bbox = None

        # In an async context, we would await. But click is sync.
        # We need to bridge sync/async if generator is async.
        # For this PoC, I'll assume we are running in a way that allows async or I'll use asyncio.run
        # But wait, Compositor.render is called from CLI which is sync.
        # I should probably make render async or handle the loop.

        import asyncio

        async def _render_layers():
            nonlocal prev_bbox
            for layer in template.layers:
                prev_bbox = await layer_renderer.render_layer(
                    canvas, layer, inputs, generator, prev_bbox
                )

        # Use existing loop if available, else new one
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
             # This is tricky if called from sync code that is already in a loop (unlikely for click)
             # but commonly we use asyncio.run for entry points.
             # If we are here, we might just be able to create a task? No, return value.
             # For CLI tool, just run_until_complete is fine.
             pass

        loop.run_until_complete(_render_layers())

        return canvas
