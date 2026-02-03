from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ImageFormat(Enum):
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"
    AVIF = "avif"
    TIFF = "tiff"
    BMP = "bmp"

class ColorSpace(Enum):
    SRGB = "sRGB"
    ADOBE_RGB = "AdobeRGB"
    CMYK = "CMYK"  # For print
    P3 = "DisplayP3"

@dataclass
class ExportConfig:
    """Flexible export configuration"""

    # Dimensions (None = keep original)
    width: Optional[int] = None
    height: Optional[int] = None
    scale: float = 1.0

    # Format
    format: ImageFormat = ImageFormat.PNG
    quality: int = 95  # 1-100 for lossy formats

    # Color
    color_space: ColorSpace = ColorSpace.SRGB
    bit_depth: int = 8  # 8 or 16

    # Optimization
    optimize: bool = True
    strip_metadata: bool = False

    # For web
    progressive: bool = False  # Progressive JPEG

    # Custom metadata
    metadata: Optional[dict] = None
