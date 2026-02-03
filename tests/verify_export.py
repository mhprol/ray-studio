from ray_studio.export import Exporter, PRESETS
from PIL import Image
import os

def test_export():
    # Create dummy image
    image = Image.new("RGBA", (2000, 2000), (255, 0, 0, 255))

    exporter = Exporter()
    output_dir = "tests/output"

    # Test 1: Preset export
    path1 = exporter.export(image, f"{output_dir}/test_ig.jpg", preset="instagram_post")
    print(f"Exported: {path1}")
    assert os.path.exists(path1)
    img1 = Image.open(path1)
    assert img1.size == (1080, 1080)
    assert img1.format == "JPEG"

    # Test 2: Custom export
    path2 = exporter.export(image, f"{output_dir}/test_custom.webp", custom_size=(500, 500), format="WEBP")
    print(f"Exported: {path2}")
    assert os.path.exists(path2)
    img2 = Image.open(path2)
    assert img2.size == (500, 500)
    assert img2.format == "WEBP"

    # Test 3: Multi export
    paths = exporter.export_multi(image, output_dir, presets=["instagram_story", "favicon"])
    for p in paths:
        print(f"Exported multi: {p}")
        assert os.path.exists(p)

    print("Export verification passed!")

if __name__ == "__main__":
    test_export()
