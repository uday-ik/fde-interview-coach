"""PostToolUse hook — run fast quality checks right after Claude edits a file.

Runs ruff (lint) then mypy (types). If either finds a REAL problem we print it to
stderr and exit non-zero, so Claude immediately sees it and fixes it — the same
tight feedback loop good CI gives a human, but per-edit.

Why this matters: when an agent changes a function signature it often forgets a
call site somewhere else. A type check catches that in seconds.

Two deliberate robustness choices:
  * We invoke the tools as `python -m ruff` / `python -m mypy` so they work even
    when their console scripts aren't on PATH (very common inside a venv).
  * If a tool simply isn't installed, we SKIP it with a note instead of failing.
    A crashing hook makes the agent burn turns trying to repair the hook itself,
    which is slow and expensive — a missing linter is a setup issue, not a code
    defect, so it must not look like one.

pytest is deliberately left out of the every-edit loop to keep it fast.
"""
import subprocess
import sys

failures = []
skipped = []

for tool, command in (
    ("ruff", [sys.executable, "-m", "ruff", "check", "app", "tests"]),
    ("mypy", [sys.executable, "-m", "mypy", "app"]),
):
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        skipped.append(tool)
        continue

    output = f"{result.stdout}{result.stderr}"
    # "No module named X" means the tool isn't installed - a setup issue, not a
    # code problem. Skip it rather than reporting a failure the agent can't fix.
    if result.returncode != 0 and f"No module named {tool}" in output:
        skipped.append(tool)
        continue
    if result.returncode != 0:
        failures.append(f"$ {' '.join(command[2:])}\n{output}".rstrip())

if skipped:
    # stdout (not stderr) - informational only, never blocks the edit.
    print(f"[checks] skipped (not installed): {', '.join(skipped)}. "
          f"Install with:  pip install {' '.join(skipped)}")

if failures:
    print("\n\n".join(failures), file=sys.stderr)
    sys.exit(2)  # non-zero -> Claude receives this output and can correct it

sys.exit(0)
