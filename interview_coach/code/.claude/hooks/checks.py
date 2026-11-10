"""PostToolUse hook: lint and type-check after the agent edits Python code.

Runs `ruff check app tests` and `mypy app`. If either fails, prints the combined
output to stderr and exits with code 2, which shows the output to the agent so it
can fix the problem. Edits to non-Python files are skipped: they can't break
either check, and running both tools on every edit is slow.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[2]
CHECKS = [
    ["ruff", "check", "app", "tests"],
    ["mypy", "app"],
]
FAIL_EXIT_CODE = 2
# Where the project's virtual environment may live (here it sits one level up).
VENV_PYTHONS = [
    PROJECT_DIR / ".venv" / "bin" / "python",
    PROJECT_DIR.parent / ".venv" / "bin" / "python",
]


def checks_python() -> str:
    """The venv's Python if there is one, else whichever Python launched the hook."""
    for candidate in VENV_PYTHONS:
        if candidate.exists():
            return str(candidate)
    return sys.executable


def edited_python_file(tool_call: dict) -> bool:
    """True if the tool call touched a .py file."""
    file_path = tool_call.get("tool_input", {}).get("file_path", "")
    return file_path.endswith(".py")


def run_check(command: list[str]) -> tuple[bool, str]:
    """Run one check with this interpreter's tools. Returns (passed, output)."""
    result = subprocess.run(
        [checks_python(), "-m", *command],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, f"$ {' '.join(command)}\n{output}"


def main() -> int:
    try:
        tool_call = json.load(sys.stdin)
    except json.JSONDecodeError:
        tool_call = {}
    if tool_call and not edited_python_file(tool_call):
        return 0
    failures = [out for passed, out in map(run_check, CHECKS) if not passed]
    if failures:
        print("\n\n".join(failures), file=sys.stderr)
        return FAIL_EXIT_CODE
    return 0


if __name__ == "__main__":
    sys.exit(main())
