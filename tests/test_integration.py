from click.testing import CliRunner
from ray_studio.cli import cli
from unittest.mock import patch, MagicMock

def test_generate_cli():
    runner = CliRunner()

    # Mock generator to avoid API calls
    with patch("ray_studio.generators.FalGenerator.generate") as mock_generate:
        # Mock return value of generate to be a red square image bytes
        from PIL import Image
        import io
        img = Image.new("RGB", (100, 100), color="red")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        mock_generate.return_value = img_byte_arr.getvalue()

        result = runner.invoke(cli, [
            "generate", "promo",
            "--dna", "examples/client_dna_example.yaml",
            "--output", "tests/output/integration_promo.png",
            "--headline", "Integration Test",
            "--cta", "Click Me"
        ])

        print(result.output)
        if result.exception:
            print(result.exception)
            import traceback
            traceback.print_tb(result.exc_info[2])

        assert result.exit_code == 0
        assert "✓ Generated" in result.output

def test_batch_cli():
    runner = CliRunner()

    with patch("ray_studio.generators.FalGenerator.generate") as mock_generate:
         # Mock return value of generate
        from PIL import Image
        import io
        img = Image.new("RGB", (100, 100), color="blue")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        mock_generate.return_value = img_byte_arr.getvalue()

        result = runner.invoke(cli, [
            "batch", "promo",
            "--dna", "examples/client_dna_example.yaml",
            "--output-dir", "tests/output/batch",
            "--presets", "instagram_post",
            "--presets", "twitter_post",
            "--headline", "Batch Test"
        ])

        print(result.output)
        if result.exception:
            print(result.exception)

        assert result.exit_code == 0
        assert "instagram_post.jpeg" in result.output
        assert "twitter_post.png" in result.output

if __name__ == "__main__":
    test_generate_cli()
    test_batch_cli()
