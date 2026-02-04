import asyncio
import click
import json
import logging
from functools import wraps

from .client import FigmaClient
from .config import FigmaConfig
from . import commands

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

@click.group()
def figma():
    """Figma Skill Module operations"""
    pass

@figma.command()
@click.option("--host", default="172.17.0.1", help="Bridge host IP")
@click.option("--port", default=3055, help="Bridge port")
@click.option("--channel", "-c", required=True, help="Channel ID from Figma plugin")
@async_command
async def status(host, port, channel):
    """Check bridge connection"""
    client = FigmaClient(host=host, port=port)
    try:
        await client.connect(channel)
        # Just connecting and joining channel is enough to verify bridge is reachable
        # We could send a ping or get_document_info to be sure
        click.echo(f"Successfully connected to {host}:{port} on channel {channel}")
    except Exception as e:
        click.echo(f"Connection failed: {e}", err=True)
        import sys; sys.exit(1)
    finally:
        await client.disconnect()

@figma.command()
@click.option("--host", default="172.17.0.1", help="Bridge host IP")
@click.option("--port", default=3055, help="Bridge port")
@click.option("--channel", "-c", required=True, help="Channel ID from Figma plugin")
@async_command
async def info(host, port, channel):
    """Get document info"""
    client = FigmaClient(host=host, port=port)
    try:
        await client.connect(channel)
        info = await commands.get_document_info(client)
        click.echo(json.dumps(info, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        import sys; sys.exit(1)
    finally:
        await client.disconnect()

@figma.command(name="scan-text")
@click.argument("node_id")
@click.option("--host", default="172.17.0.1", help="Bridge host IP")
@click.option("--port", default=3055, help="Bridge port")
@click.option("--channel", "-c", required=True, help="Channel ID from Figma plugin")
@async_command
async def scan_text(node_id, host, port, channel):
    """Scan text nodes under a specific node"""
    client = FigmaClient(host=host, port=port)
    try:
        await client.connect(channel)
        result = await commands.scan_text_nodes(client, node_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        import sys; sys.exit(1)
    finally:
        await client.disconnect()

@figma.command(name="set-text")
@click.argument("target")
@click.argument("text")
@click.option("--host", default="172.17.0.1", help="Bridge host IP")
@click.option("--port", default=3055, help="Bridge port")
@click.option("--channel", "-c", required=True, help="Channel ID from Figma plugin")
@click.option("--is-path", is_flag=True, help="Treat TARGET as a template path instead of Node ID")
@async_command
async def set_text_cmd(target, text, host, port, channel, is_path):
    """Modify text content of a node"""
    client = FigmaClient(host=host, port=port)
    config = FigmaConfig()

    try:
        await client.connect(channel)

        if is_path:
            result = await commands.set_text_by_path(client, config, target, text)
        else:
            result = await commands.set_text(client, target, text)

        click.echo(f"Success: {json.dumps(result)}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        import sys; sys.exit(1)
    finally:
        await client.disconnect()

@figma.command()
@click.argument("name", default="My Project")
@click.option("--path", default="Ray/figma-project.json", help="Path to create config file")
def init(name, path):
    """Initialize figma-project.json"""
    try:
        FigmaConfig.create_template(path, name)
        click.echo(f"Created config at {path}")
    except Exception as e:
        click.echo(f"Error creating config: {e}", err=True)
        import sys; sys.exit(1)
