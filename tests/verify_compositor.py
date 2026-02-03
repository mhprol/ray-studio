from ray_studio.compositor import Compositor
from ray_studio.templates.base import Template, Layer, Layout
from ray_studio.dna import BrandDNA
from ray_studio.dna.schema import BrandIdentity, Colors, Fonts, Logo, Audience, ContentStrategy
from PIL import Image

def test_compositor():
    # Mock DNA
    dna = BrandDNA(
        brand=BrandIdentity(
            name="Test Brand",
            tagline="Test Tagline",
            colors=Colors(
                primary="#FF0000",
                secondary="#00FF00",
                accent="#0000FF",
                background="#FFFFFF",
                text="#000000"
            ),
            fonts=Fonts(heading="Arial", body="Arial", accent="Arial"),
            tone="bold",
            expression="bold",
            logo=Logo(primary="logo.png")
        ),
        audience=Audience(description="", pain_points=[], desires=[]),
        products=[],
        content=ContentStrategy(hashtags=[], cta_phrases=[])
    )

    # Mock Template
    template = Template(
        name="test_template",
        description="test",
        category="test",
        layout=Layout(),
        layers=[
            Layer(type="background", source="solid", color="{dna.brand.colors.primary}"),
            Layer(type="text", content="Hello {input.name}", font="{dna.brand.fonts.heading}", size=40, color="#FFFFFF", position="center")
        ],
        inputs={}
    )

    inputs = {"name": "World"}

    compositor = Compositor()
    image = compositor.render(template, dna, inputs)

    assert isinstance(image, Image.Image)
    assert image.size == (1080, 1080)

    # Check if pixel (0,0) is primary color (Red)
    # PIL returns (R, G, B, A)
    pixel = image.getpixel((0, 0))
    print(f"Pixel (0,0): {pixel}")
    assert pixel[:3] == (255, 0, 0)

    print("Compositor verification passed!")

if __name__ == "__main__":
    test_compositor()
