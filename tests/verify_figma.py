import asyncio
import json
import os
import unittest
import uuid
from unittest.mock import MagicMock, AsyncMock, patch
from websockets.connection import State

from ray_studio.figma.client import FigmaClient
from ray_studio.figma.config import FigmaConfig
from ray_studio.figma import commands

class TestFigma(unittest.IsolatedAsyncioTestCase):

    async def test_client_connect_and_send(self):
        with patch("websockets.connect", new_callable=AsyncMock) as mock_connect:

            # Setup response
            response_payload = {
                "message": {
                    "id": "test-id",
                    "result": {"success": True}
                }
            }

            # Create a class that mimics the websocket protocol
            class MockProtocol:
                def __init__(self):
                    self.state = State.OPEN
                    self.sent = []

                async def send(self, msg):
                    self.sent.append(msg)

                async def close(self):
                    self.state = State.CLOSED

                async def __aiter__(self):
                    # Simulate delay before response
                    await asyncio.sleep(0.05)
                    yield json.dumps(response_payload)
                    # Keep yielding nothing or sleep to simulate open connection
                    # If we exit, the client loop might treat it as closed connection
                    while self.state != State.CLOSED:
                        await asyncio.sleep(0.1)

            mock_ws = MockProtocol()
            mock_connect.return_value = mock_ws

            with patch("uuid.uuid4", return_value="test-id"):
                client = FigmaClient()

                await client.connect("channel-123")

                # Check join
                # Wait a bit for connect/join to happen
                await asyncio.sleep(0.01)
                self.assertEqual(len(mock_ws.sent), 1)
                join_msg = json.loads(mock_ws.sent[0])
                self.assertEqual(join_msg["type"], "join")

                # Send command
                result = await client.send_command("test_cmd", {"foo": "bar"})

                self.assertEqual(result, {"success": True})

                # Verify command message sent
                self.assertEqual(len(mock_ws.sent), 2)
                cmd_msg = json.loads(mock_ws.sent[1])
                self.assertEqual(cmd_msg["message"]["command"], "test_cmd")
                self.assertEqual(cmd_msg["message"]["id"], "test-id")

                await client.disconnect()

    def test_config(self):
        # Create a dummy config file
        config_path = "test_figma_project.json"

        try:
            FigmaConfig.create_template(config_path, "Test Project")

            # Load config
            config = FigmaConfig(config_path)
            self.assertEqual(config.project.name, "Test Project")

            # Add some data manually to file to test resolution
            config.project.templates = {
                "social": {
                    "children": {
                        "post": {
                            "nodeId": "1:1"
                        }
                    }
                },
                "simple": {
                    "nodeId": "2:2"
                }
            }
            config.save()

            # Reload and test resolution
            config = FigmaConfig(config_path)

            # Test direct
            self.assertEqual(config.get_node_id("simple"), "2:2")

            # Test nested
            self.assertEqual(config.get_node_id("social.post"), "1:1")

            # Test invalid
            self.assertIsNone(config.get_node_id("social.missing"))
            self.assertIsNone(config.get_node_id("invalid"))

        finally:
            if os.path.exists(config_path):
                os.remove(config_path)

    async def test_commands(self):
        client = MagicMock(spec=FigmaClient)
        client.send_command = AsyncMock(return_value={"info": "doc"})

        info = await commands.get_document_info(client)
        self.assertEqual(info, {"info": "doc"})
        client.send_command.assert_called_with("get_document_info", {})

        client.send_command.return_value = {"success": True}
        await commands.set_text(client, "1:1", "Hello")
        client.send_command.assert_called_with("set_text_content", {"nodeId": "1:1", "text": "Hello"})

        # Test export
        import base64
        dummy_data = base64.b64encode(b"fake image data").decode("utf-8")
        client.send_command.return_value = {"data": dummy_data}

        output_file = "test_export.png"
        try:
            path = await commands.export_node(client, "1:1", "png", output_file)
            self.assertTrue(os.path.exists(output_file))
            with open(output_file, "rb") as f:
                self.assertEqual(f.read(), b"fake image data")
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

if __name__ == "__main__":
    unittest.main()
