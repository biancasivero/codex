"""Entry point for running the Agent Cards MCP server used in tests."""

from __future__ import annotations

import sys
from pathlib import Path

# The a2a_mcp package lives under ``backup/python`` in this repository. Add the
# package root to ``sys.path`` so that ``from a2a_mcp.mcp.server`` works when
# executing this file directly.
sys.path.append(
    str(Path(__file__).resolve().parents[3] / "backup/python/agents/a2a_mcp/src")
)

from a2a_mcp.mcp.server import serve


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="MCP Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address")
    parser.add_argument("--port", type=int, default=10000, help="Port number")
    parser.add_argument(
        "--transport", type=str, default="sse", help="Transport mechanism"
    )
    args = parser.parse_args()

    serve(args.host, args.port, args.transport)


if __name__ == "__main__":
    main()
