"""MCP server exposing database operations as tools.

Run standalone: python mcp_server/db_server.py
The server communicates via stdio (default FastMCP transport).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mcp.server.fastmcp import FastMCP
from tools.db_tools import get_schema as _get_schema, execute_query as _execute_query

mcp = FastMCP("nl-to-sql-db-server")


@mcp.tool()
def get_schema() -> str:
    """Return the database schema: tables, columns, types, and foreign keys."""
    return _get_schema()


@mcp.tool()
def execute_query(sql: str) -> str:
    """Execute a SELECT SQL query and return formatted results.

    Returns rows as a pipe-delimited table, or an ERROR: prefixed message on failure.
    """
    result, error = _execute_query(sql)
    if error:
        return f"ERROR: {error}"
    return result


if __name__ == "__main__":
    mcp.run()
