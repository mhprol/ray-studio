from PIL import Image, ImageFilter

class EffectRenderer:
    """Applies effects to images."""

    @staticmethod
    def apply_blur(image: Image.Image, radius: int = 2) -> Image.Image:
        return image.filter(ImageFilter.GaussianBlur(radius))
