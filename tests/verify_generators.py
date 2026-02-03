import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from ray_studio.generators import FalGenerator, get_generator

async def test_fal_generator():
    api_key = "fake_key"
    generator = FalGenerator(api_key=api_key)

    # Mock httpx.AsyncClient
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()  # Use AsyncMock for the client instance
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        # Mock post response
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {"images": [{"url": "http://fake.url/image.png"}]}
        mock_post_response.raise_for_status = MagicMock()
        mock_client.post.return_value = mock_post_response

        # Mock get response (download)
        mock_get_response = MagicMock()
        mock_get_response.content = b"fake_image_bytes"
        mock_get_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_get_response

        # Test generate
        result = await generator.generate("test prompt", size=(800, 600))

        assert result == b"fake_image_bytes"

        # Verify post call
        mock_client.post.assert_called_once()
        args, kwargs = mock_client.post.call_args
        assert kwargs["json"]["prompt"] == "test prompt"
        assert kwargs["json"]["image_size"] == {"width": 800, "height": 600}

        print("FalGenerator test passed!")

def test_get_generator():
    gen = get_generator()
    assert isinstance(gen, FalGenerator)
    print("get_generator test passed!")

if __name__ == "__main__":
    test_get_generator()
    asyncio.run(test_fal_generator())
