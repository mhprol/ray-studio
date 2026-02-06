import asyncio
import json
import logging
import uuid
from typing import Dict, Any, Optional

import websockets

logger = logging.getLogger(__name__)

class FigmaClient:
    """
    WebSocket client for communicating with the Figma bridge.
    Handles connection, reconnection, and command/response correlation.
    """
    def __init__(self, host: str = "172.17.0.1", port: int = 3055):
        self.uri = f"ws://{host}:{port}"
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.channel: Optional[str] = None
        self.pending_requests: Dict[str, asyncio.Future] = {}
        self.listen_task: Optional[asyncio.Task] = None
        self.running = False

    async def connect(self, channel: str):
        """Connect to the bridge and join the specified channel."""
        self.channel = channel
        self.running = True
        await self._connect_socket()
        self.listen_task = asyncio.create_task(self._listen_loop())

    async def _connect_socket(self):
        """Internal method to establish WebSocket connection and join channel."""
        logger.info(f"Connecting to Figma bridge at {self.uri}...")
        self.websocket = await websockets.connect(self.uri)

        # Join channel
        await self.websocket.send(json.dumps({
            "type": "join",
            "channel": self.channel
        }))
        logger.info(f"Joined channel: {self.channel}")

    async def disconnect(self):
        """Disconnect from the bridge and stop the listen loop."""
        self.running = False
        if self.listen_task:
            self.listen_task.cancel()
            try:
                await self.listen_task
            except asyncio.CancelledError:
                pass

        if self.websocket:
            await self.websocket.close()
            self.websocket = None

    async def _listen_loop(self):
        """Background loop to listen for messages and handle reconnection."""
        while self.running:
            try:
                # Reconnect if needed
                if not self.websocket or self.websocket.state.name == 'CLOSED':
                    try:
                        await self._connect_socket()
                    except Exception as e:
                        logger.warning(f"Connection failed, retrying in 3s: {e}")
                        await asyncio.sleep(3)
                        continue

                async for message in self.websocket:
                    try:
                        data = json.loads(message)
                        # We are interested in "message" type responses that have an ID
                        # Structure: { "type": "message", "message": { "id": "...", "result": ... } }
                        # Or broadcast messages that might look different
                        if data.get("message") and "id" in data["message"]:
                            msg_id = data["message"]["id"]
                            if msg_id in self.pending_requests:
                                future = self.pending_requests.pop(msg_id)
                                if not future.done():
                                    future.set_result(data["message"])
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")

            except websockets.ConnectionClosed:
                logger.warning("WebSocket connection closed. Reconnecting...")
                self.websocket = None
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Unexpected error in listen loop: {e}")
                await asyncio.sleep(1)

    async def send_command(self, command: str, params: Dict[str, Any], timeout: float = 10.0) -> Any:
        """
        Send a command to Figma and await the response.

        Args:
            command: The command name (e.g., 'scan_text_nodes')
            params: Dictionary of parameters for the command
            timeout: Timeout in seconds

        Returns:
            The 'result' field from the response
        """
        if not self.running:
             raise RuntimeError("Client is not running. Call connect() first.")

        # Wait for connection if not connected (up to timeout)
        start_time = asyncio.get_running_loop().time()
        while not self.websocket or self.websocket.state.name != 'OPEN':
            if asyncio.get_running_loop().time() - start_time > timeout:
                 raise ConnectionError("Timed out waiting for connection")
            await asyncio.sleep(0.1)

        request_id = str(uuid.uuid4())
        payload = {
            "type": "message",
            "channel": self.channel,
            "message": {
                "command": command,
                "id": request_id,
                "params": params
            }
        }

        future = asyncio.get_running_loop().create_future()
        self.pending_requests[request_id] = future

        try:
            await self.websocket.send(json.dumps(payload))
            response = await asyncio.wait_for(future, timeout)

            if "error" in response:
                 raise Exception(response["error"])

            return response.get("result")
        except asyncio.TimeoutError:
            if request_id in self.pending_requests:
                del self.pending_requests[request_id]
            raise TimeoutError(f"Command {command} timed out")
        except Exception as e:
            if request_id in self.pending_requests:
                del self.pending_requests[request_id]
            raise e
