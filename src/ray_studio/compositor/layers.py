from PIL import Image, ImageDraw
import io
import httpx
from typing import Dict, Any, Tuple
from ..templates.base import Layer
from ..dna.schema import BrandDNA
from .text import TextRenderer

class LayerRenderer:
    """Handles rendering of individual layers."""

    def __init__(self, dna: BrandDNA):
        self.dna = dna
        self.text_renderer = TextRenderer()

    def resolve_value(self, value: Any, inputs: Dict[str, Any]) -> Any:
        """Resolve variables in value string like {input.headline} or {dna.colors.primary}."""
        if not isinstance(value, str):
            return value

        # Check if the entire string is a key without braces (common in YAML props)
        if value.startswith("dna.") or value.startswith("input."):
             # Try to resolve it directly
             resolved = self._lookup(value, inputs)
             if resolved is not None:
                 return resolved

        # Replace embedded variables {dna.x.y}
        import re
        def replace_match(match):
            key = match.group(1)
            val = self._lookup(key, inputs)
            return str(val) if val is not None else match.group(0)

        return re.sub(r"\{([a-zA-Z0-9_\.]+)\}", replace_match, value)

    def _lookup(self, key: str, inputs: Dict[str, Any]) -> Any:
        """Look up a value by dot notation key."""
        if key.startswith("input."):
            input_key = key[6:]
            return inputs.get(input_key)

        if key.startswith("dna."):
            # Traversal for DNA
            parts = key.split(".")
            # parts[0] is 'dna'
            obj = self.dna
            try:
                for part in parts[1:]:
                     if hasattr(obj, part):
                         obj = getattr(obj, part)
                     elif isinstance(obj, dict) and part in obj:
                         obj = obj[part]
                     else:
                         return None
                return obj
            except Exception:
                return None
        return None

    async def render_layer(
        self,
        canvas: Image.Image,
        layer: Layer,
        inputs: Dict[str, Any],
        generator,
        prev_bbox: Tuple[int, int, int, int] = None
    ) -> Tuple[int, int, int, int]:
        """
        Render a layer onto the canvas.
        Returns the bounding box of the rendered content (x1, y1, x2, y2).
        """
        draw = ImageDraw.Draw(canvas)
        width, height = canvas.size

        # Resolve common properties
        content = self.resolve_value(layer.content, inputs) if layer.content else None
        color = self.resolve_value(layer.color, inputs) if layer.color else "#000000"
        background_color = self.resolve_value(layer.background, inputs) if layer.background else None
        source = self.resolve_value(layer.source, inputs) if layer.source else None

        # Determine position
        x, y = 0, 0

        if layer.position == "center":
            x = width / 2
            y = height / 2
        elif layer.position == "top-left":
            x = layer.margin or 0
            y = layer.margin or 0
        elif layer.position == "bottom-center":
            x = width / 2
            y = height - (layer.margin_bottom or 0) - (layer.padding[1]*2 if isinstance(layer.padding, list) else 0) # Rough estimate
        elif layer.position == "below_previous" and prev_bbox:
            x = width / 2 # Default to center x for now
            y = prev_bbox[3] + (layer.margin_top or 0)
        elif layer.position == "bottom-right":
            x = width - (layer.margin or 0)
            y = height - (layer.margin or 0)
        elif layer.position == "left":
            x = 0
            y = 0 # Fills height usually
        elif layer.position == "right-top":
             x = width / 2 # Split layout assumption
             y = (layer.margin_top or 0)

        bbox = (int(x), int(y), int(x), int(y))

        if layer.type == "background":
            if source == "solid":
                canvas.paste(Image.new("RGBA", canvas.size, color or background_color), (0, 0))
                bbox = (0, 0, width, height)
            elif source == "ai_generate" and generator:
                prompt = self.resolve_value(layer.prompt_template, inputs)
                try:
                    img_bytes = await generator.generate(prompt, size=canvas.size)
                    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
                    img = img.resize(canvas.size) # Ensure fit
                    canvas.paste(img, (0, 0))
                    bbox = (0, 0, width, height)
                except Exception as e:
                    print(f"Failed to generate background: {e}")
                    # Fallback
                    canvas.paste(Image.new("RGBA", canvas.size, "#CCCCCC"), (0, 0))

        elif layer.type == "text" and content:
            font_name = self.resolve_value(layer.font, inputs)
            max_w = layer.max_width
            if isinstance(max_w, str) and max_w.endswith("%"):
                max_w = int(width * int(max_w[:-1]) / 100)

            # Anchor mapping
            anchor = "center" if layer.position == "center" or layer.position == "bottom-center" or layer.position == "below_previous" else None
            if layer.position == "right-top" or layer.position == "left":
                 anchor = None # Default left align

            end_y = self.text_renderer.draw_text(
                draw,
                content,
                (x, y),
                font_name,
                layer.size,
                color,
                max_width=max_w,
                anchor=anchor
            )
            # Rough bbox estimation
            bbox = (int(x), int(y), int(x) + (max_w or 100), int(end_y))

        elif layer.type == "cta_button":
            # Draw rect
            # Determine text size first to size the button
            text = self.resolve_value(layer.text, inputs)
            font_size = 24 # Default
            # Calculate button size
            btn_w, btn_h = 200, 60 # Defaults

            pad_x, pad_y = (20, 10)
            if isinstance(layer.padding, list):
                pad_x, pad_y = layer.padding

            # Draw button rect
            btn_x = x - btn_w / 2
            btn_y = y - btn_h

            draw.rectangle(
                [btn_x, btn_y, btn_x + btn_w, btn_y + btn_h],
                fill=background_color,
                outline=None,
                width=0
            )

            # Draw text
            self.text_renderer.draw_text(
                draw,
                text,
                (x, y - btn_h/2),
                "Inter", # Default
                font_size,
                color,
                anchor="center"
            )
            bbox = (int(btn_x), int(btn_y), int(btn_x + btn_w), int(btn_y + btn_h))

        elif layer.type == "logo" or layer.type == "image":
             # In a real app, load image from path or URL
             # Here we placeholder with a rect
             w, h = 100, 100
             if isinstance(layer.size, list):
                 w_val, h_val = layer.size
                 w = w_val if isinstance(w_val, int) else 100
                 h = h_val if isinstance(h_val, int) else 100

                 if isinstance(layer.size[0], str) and layer.size[0].endswith("%"):
                     w = int(width * int(layer.size[0][:-1]) / 100)
                 if isinstance(layer.size[1], str) and layer.size[1].endswith("%"):
                     h = int(height * int(layer.size[1][:-1]) / 100)

             draw.rectangle([x, y, x + w, y + h], fill="#888888", outline="black")
             bbox = (int(x), int(y), int(x + w), int(y + h))

        return bbox
