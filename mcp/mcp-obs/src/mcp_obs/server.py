"""Stdio MCP server exposing observability tools for VictoriaLogs and VictoriaTraces."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from mcp_obs.observability import ObsClient
from mcp_obs.settings import get_settings
from mcp_obs.tools import TOOL_SPECS, TOOLS_BY_NAME


def _text(data: Any) -> list[TextContent]:
    """Convert data to MCP text content."""
    import json

    if hasattr(data, "model_dump"):
        payload = data.model_dump()
    else:
        payload = data
    return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False, indent=2))]


def create_server(client: ObsClient) -> Server:
    """Create the MCP server with observability tools."""
    server = Server("obs")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [spec.as_tool() for spec in TOOL_SPECS]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[TextContent]:
        spec = TOOLS_BY_NAME.get(name)
        if spec is None:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        try:
            args = spec.model.model_validate(arguments or {})
            return await spec.handler(client, args)
        except Exception as exc:
            return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]

    _ = list_tools, call_tool
    return server


async def main() -> None:
    """Main entry point."""
    settings = get_settings()
    client = ObsClient(settings)
    try:
        server = create_server(client)
        async with stdio_server() as (read_stream, write_stream):
            init_options = server.create_initialization_options()
            await server.run(read_stream, write_stream, init_options)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
