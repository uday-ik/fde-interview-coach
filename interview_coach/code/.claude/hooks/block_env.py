"""PreToolUse hook: block the agent from reading .env files.

Claude Code sends the tool call as JSON on stdin. Exit code 2 blocks the call
and shows stderr to the agent; exit code 0 lets it through.
"""
from __future__ import annotations

import json
import sys

SECRET_MARKER = ".env"
ALLOWED_MARKER = ".env.example"
BLOCK_EXIT_CODE = 2


def is_blocked(file_path: str) -> bool:
    """True for paths containing ".env", except ".env.example"."""
    return SECRET_MARKER in file_path and ALLOWED_MARKER not in file_path


def main() -> int:
    try:
        tool_call = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0  # not a call we can read: don't block
    file_path = tool_call.get("tool_input", {}).get("file_path", "")
    if is_blocked(file_path):
        print(
            f"Blocked: reading '{file_path}' is not allowed (it may contain secrets). "
            "Use .env.example to see which variables exist.",
            file=sys.stderr,
        )
        return BLOCK_EXIT_CODE
    return 0


if __name__ == "__main__":
    sys.exit(main())
