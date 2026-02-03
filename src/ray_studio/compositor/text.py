from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

class TextRenderer:
    """Handles text rendering with wrapping and font loading."""

    # Simple font mapping for now. In a real app, this would be more robust.
    FONTS = {
        "Montserrat": "arial.ttf", # Fallback
        "Inter": "arial.ttf",
        "Playfair Display": "arial.ttf",
    }

    @staticmethod
    def get_font(font_name: str, size: int) -> ImageFont.FreeTypeFont:
        """Load font."""
        # Try to load system font or fallback to default
        try:
            # This works on Linux usually
            return ImageFont.truetype("DejaVuSans.ttf", size)
        except OSError:
            try:
                return ImageFont.truetype("arial.ttf", size)
            except OSError:
                return ImageFont.load_default()

    @staticmethod
    def draw_text(
        draw: ImageDraw.ImageDraw,
        text: str,
        position: tuple,
        font_name: str,
        size: int,
        color: str,
        max_width: int = None,
        anchor: str = None
    ):
        font = TextRenderer.get_font(font_name, size)

        lines = []
        if max_width:
            # Estimate char width (very rough)
            avg_char_width = size * 0.6
            width_in_chars = int(max_width / avg_char_width)
            lines = textwrap.wrap(text, width=width_in_chars)
        else:
            lines = [text]

        y = position[1]
        line_height = size * 1.2

        for line in lines:
            # If anchor is center, we need to calculate x
            x = position[0]
            if anchor == "center":
                # bbox = draw.textbbox((0, 0), line, font=font)
                # w = bbox[2] - bbox[0]
                # x -= w / 2
                # ImageDraw supports anchor="mm" for middle
                draw.text((x, y), line, font=font, fill=color, anchor="mm")
            else:
                draw.text((x, y), line, font=font, fill=color)

            y += line_height

        return y # Return new Y position
