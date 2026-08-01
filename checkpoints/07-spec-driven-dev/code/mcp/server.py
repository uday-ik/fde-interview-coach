"""MCP server (Module 5) — serve the interview guides to Claude Code.

MCP (Model Context Protocol) is how an AI agent reaches data that lives OUTSIDE
its codebase. Here we expose the markdown guides in ../resources so Claude can
pull the right guidance on demand instead of us pasting it into a prompt.

Try it:
    python mcp/server.py                      # run the server
    npx @modelcontextprotocol/inspector python mcp/server.py    # poke at it in a UI

Then register it with Claude Code so the tools show up in your session.
"""
from __future__ import annotations

from pathlib import Path

from fastmcp import FastMCP

# The guides live one level up, in coach/resources/
RESOURCES = Path(__file__).resolve().parent.parent / "resources"

mcp = FastMCP("interview-guides")


@mcp.tool
def list_guides() -> list[str]:
    """List the available interview guide names, e.g. 'decomposition-guide'."""
    return sorted(path.stem for path in RESOURCES.glob("*.md"))


@mcp.tool
def get_guide(name: str) -> str:
    """Return the full markdown text of one guide, by name."""
    path = RESOURCES / f"{name}.md"
    if not path.exists():
        raise ValueError(f"No guide named {name!r}. Call list_guides() to see the options.")
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
