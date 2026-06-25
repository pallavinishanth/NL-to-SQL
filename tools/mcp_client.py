"""Sync wrappers around the MCP database server.

Each call spawns the MCP server as a subprocess via stdio, makes the tool call,
and exits. Agents import from here instead of touching db_tools directly.
"""

import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

_SERVER_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "mcp_server", "db_server.py")


async def _call_tool(tool_name: str, arguments: dict) -> str:
    params = StdioServerParameters(
        command=sys.executable,
        args=[_SERVER_SCRIPT],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return result.content[0].text


def _run(coro):
    return asyncio.run(coro)


def get_schema() -> str:
    return _run(_call_tool("get_schema", {}))


def execute_query(sql: str) -> tuple[str, str]:
    result = _run(_call_tool("execute_query", {"sql": sql}))
    if result.startswith("ERROR: "):
        return "", result[len("ERROR: "):]
    return result, ""
