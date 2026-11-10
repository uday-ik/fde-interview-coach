"""MCP server "interview-guides": exposes the study guides in resources/.

Run it (stdio):  python mcp/server.py

Do not add an __init__.py to this folder: it is named `mcp`, like the `mcp`
package FastMCP depends on, and must stay a plain folder so it can't shadow it.
"""
from __future__ import annotations

from pathlib import Path

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

# This file lives in code/mcp/, so the guides are in ../resources/.
GUIDES_DIR = Path(__file__).resolve().parent.parent / "resources"
GUIDE_SUFFIX = ".md"

server = FastMCP("interview-guides")


def _guide_names() -> list[str]:
    """Names (without .md) of every guide in resources/, sorted."""
    return sorted(path.stem for path in GUIDES_DIR.glob(f"*{GUIDE_SUFFIX}"))


@server.tool
def list_guides() -> list[str]:
    """List the available interview study guides by name."""
    return _guide_names()


@server.tool
def get_guide(name: str) -> str:
    """Return the full markdown of one guide. `name` is one of list_guides()."""
    # Checking against the known names also blocks paths like "../CLAUDE".
    names = _guide_names()
    if name not in names:
        raise ToolError(f"No guide named '{name}'. Available guides: {', '.join(names)}")
    return (GUIDES_DIR / f"{name}{GUIDE_SUFFIX}").read_text(encoding="utf-8")


if __name__ == "__main__":
    server.run()
