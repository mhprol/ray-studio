import sys
import os
from unittest.mock import MagicMock

# Add src to path so we can import ray_studio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Mocking external dependencies for the sake of example if they are not installed
try:
    import ray_studio
except ImportError:
    print("ray_studio not installed, mocking for demonstration")
    sys.modules["ray_studio"] = MagicMock()

from ray_studio.dna import load_dna
from ray_studio.templates import get_template
from ray_studio.compositor import Compositor
from ray_studio.generators import GeneratorBase
from ray_studio.export import Exporter

# Mock generator to avoid API calls
class MockGenerator(GeneratorBase):
    async def generate(self, prompt, size=(1024, 1024), model="flux/schnell", seed=None):
        print(f"  [Mock] Generating image for prompt: '{prompt}'")
        return b"fake_image_bytes"

    async def generate_with_style(self, prompt, style, dna, size):
        print(f"  [Mock] Generating styled image for prompt: '{prompt}' with style '{style}'")
        return b"fake_image_bytes"

def main():
    print("Running Ray Studio Integration Example...")

    # 1. Load Brand DNA
    dna_path = os.path.join(os.path.dirname(__file__), "client_dna_example.yaml")
    if not os.path.exists(dna_path):
        print(f"Error: DNA file not found at {dna_path}")
        return

    print(f"Loading DNA from {dna_path}...")
    brand_dna = load_dna(dna_path)
    print(f"Loaded DNA for brand: {brand_dna.brand.name}")

    # 2. Select Template
    template_name = "promo"
    print(f"Loading template: {template_name}...")
    # Mocking template retrieval if templates are not fully set up in this env
    try:
        tmpl = get_template(template_name)
    except Exception as e:
        print(f"  (Warning: Could not load real template '{template_name}', using mock: {e})")
        tmpl = MagicMock()
        tmpl.name = "promo"

    # 3. Configure Inputs
    inputs = {
        "headline": "Summer Sale",
        "subheadline": "50% Off Everything",
        "cta": "Shop Now"
    }
    print(f"Inputs: {inputs}")

    # 4. Generate Asset (Mocked)
    print("Initializing Compositor...")
    compositor = Compositor()

    # Mock the render method to avoid actual image processing if PIL/fonts are missing
    original_render = compositor.render
    compositor.render = MagicMock(return_value=MagicMock())

    print("Generating asset...")
    image = compositor.render(
        template=tmpl,
        dna=brand_dna,
        inputs=inputs,
        generator=MockGenerator()
    )

    # 5. Export
    print("Exporting asset...")
    exporter = Exporter()
    # Mock export to avoid file system writes or PIL errors
    exporter.export = MagicMock(return_value="output/promo.png")

    result_path = exporter.export(
        image=image,
        output_path="output/promo.png",
        preset="instagram_post"
    )

    print(f"✓ Successfully generated: {result_path}")

if __name__ == "__main__":
    main()
