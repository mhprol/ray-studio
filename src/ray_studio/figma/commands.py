import base64
import logging
from typing import Dict, Any, Optional

from .client import FigmaClient
from .config import FigmaConfig

logger = logging.getLogger(__name__)

async def get_document_info(client: FigmaClient) -> Dict[str, Any]:
    """Get information about the current Figma document."""
    return await client.send_command("get_document_info", {})

async def scan_text_nodes(client: FigmaClient, node_id: str) -> Any:
    """Scan for text nodes within a given node."""
    return await client.send_command("scan_text_nodes", {"nodeId": node_id})

async def set_text(client: FigmaClient, node_id: str, text: str) -> Any:
    """Set the text content of a specific node."""
    return await client.send_command("set_text_content", {"nodeId": node_id, "text": text})

async def set_text_by_path(client: FigmaClient, config: FigmaConfig, template_path: str, text: str) -> Any:
    """
    Set text content resolving the node ID from the config via a template path.
    Example path: 'socialMedia.postPreview1.headline'
    """
    node_id = config.get_node_id(template_path)
    if not node_id:
        raise ValueError(f"Could not resolve template path: {template_path}")
    logger.info(f"Resolved {template_path} to node ID {node_id}")
    return await set_text(client, node_id, text)

async def export_node(client: FigmaClient, node_id: str, format: str, output_path: str) -> str:
    """
    Export a node to a file.
    Assumes the bridge returns a dictionary with 'data' field containing base64 encoded image data.
    """
    result = await client.send_command("export_node", {"nodeId": node_id, "format": format})

    if isinstance(result, dict) and "data" in result:
        try:
            data = base64.b64decode(result["data"])
            with open(output_path, "wb") as f:
                f.write(data)
            return output_path
        except Exception as e:
            logger.error(f"Failed to decode or write export data: {e}")
            raise e

    # Fallback if result isn't data (e.g. maybe it's a URL or success message)
    logger.info(f"Export command finished. Result: {result}")
    return str(result)
