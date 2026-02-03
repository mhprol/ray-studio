from PIL import Image
import os
from .formats import ExportConfig, ImageFormat, ColorSpace
from .presets import PRESETS
from typing import Optional

class Exporter:
    """Flexible export with any format/size combination"""

    def export(
        self,
        image: Image.Image,
        output_path: str,
        config: ExportConfig = None,
        preset: str = None,
        custom_size: tuple[int, int] = None,
        **kwargs
    ) -> str:
        """
        Export image with maximum flexibility.
        """
        # Build config from preset or defaults
        if config:
            cfg = config
        elif preset:
            # We copy because we might modify it
            import copy
            cfg = copy.copy(PRESETS.get(preset, ExportConfig()))
        else:
            cfg = ExportConfig()

        # Apply overrides
        for key, value in kwargs.items():
            if hasattr(cfg, key):
                # Handle Enum conversion
                if key == "format" and isinstance(value, str):
                    try:
                         # Try to match by value
                         value = ImageFormat(value.lower())
                    except ValueError:
                         pass
                if key == "color_space" and isinstance(value, str):
                    try:
                        value = ColorSpace(value)
                    except ValueError:
                        pass

                setattr(cfg, key, value)

        if custom_size:
            cfg.width, cfg.height = custom_size

        # Process image
        processed = self._process(image, cfg)

        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Save
        return self._save(processed, output_path, cfg)

    def export_multi(
        self,
        image: Image.Image,
        output_dir: str,
        presets: list[str],
        naming: str = "{preset}"
    ) -> list[str]:
        """Export to multiple formats/sizes at once"""
        paths = []
        for preset in presets:
            if preset not in PRESETS:
                print(f"Warning: Preset {preset} not found. Skipping.")
                continue

            cfg = PRESETS[preset]
            ext = cfg.format.value
            filename = naming.format(preset=preset) + f".{ext}"
            path = os.path.join(output_dir, filename)
            paths.append(self.export(image, path, preset=preset))
        return paths

    def _process(self, image: Image.Image, config: ExportConfig) -> Image.Image:
        """Process image (resize, color space)."""
        img = image.copy()

        # Resize
        target_w, target_h = config.width, config.height
        if target_w and target_h:
            img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        elif config.scale != 1.0:
            w, h = img.size
            img = img.resize((int(w * config.scale), int(h * config.scale)), Image.Resampling.LANCZOS)

        # Color Space
        if config.color_space == ColorSpace.CMYK:
             if img.mode != "CMYK":
                 img = img.convert("CMYK")
        elif config.color_space == ColorSpace.SRGB:
             if img.mode != "RGB":
                 img = img.convert("RGB")

        return img

    def _save(self, image: Image.Image, path: str, config: ExportConfig) -> str:
        """Save image to disk."""
        save_kwargs = {}

        # Format mapping
        # Ensure format is Enum
        if isinstance(config.format, str):
             try:
                 config.format = ImageFormat(config.format.lower())
             except ValueError:
                 # Fallback if invalid string
                 pass

        fmt = config.format.value.upper() if isinstance(config.format, ImageFormat) else str(config.format).upper()

        if fmt == "JPEG":
            fmt = "JPEG"
            save_kwargs["quality"] = config.quality
            save_kwargs["optimize"] = config.optimize
            if config.progressive:
                save_kwargs["progressive"] = True
        elif fmt == "PNG":
            fmt = "PNG"
            save_kwargs["optimize"] = config.optimize
        elif fmt == "WEBP":
            fmt = "WEBP"
            save_kwargs["quality"] = config.quality
            save_kwargs["method"] = 6 # Max compression
        elif fmt == "TIFF":
            fmt = "TIFF"

        # Handle alpha for JPEG
        if fmt == "JPEG" and image.mode in ("RGBA", "LA"):
             background = Image.new("RGB", image.size, (255, 255, 255))
             background.paste(image, mask=image.split()[-1])
             image = background

        try:
            image.save(path, format=fmt, **save_kwargs)
        except Exception as e:
            # Fallback if format is not supported by extension
            image.save(path, **save_kwargs)

        return path
