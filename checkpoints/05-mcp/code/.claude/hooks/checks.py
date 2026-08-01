"""PostToolUse hook — run fast quality checks right after Claude edits a file.

Runs ruff (lint) then mypy (types). If either fails we print the output to
stderr and exit non-zero, so Claude immediately SEES the problem and fixes it —
the same tight feedback loop good CI gives a human, but per-edit.

Why this matters: when an agent changes a function signature it often forgets a
call site somewhere else. A type check catches that in seconds.

pytest is deliberately left out of the every-edit loop to keep it fast; run it
as its own step, or add it here if you want it enforced too.
"""
import subprocess
import sys

failures = []
for command in (["ruff", "check", "app", "tests"], ["mypy", "app"]):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        failures.append(f"$ {' '.join(command)}\n{result.stdout}{result.stderr}".rstrip())

if failures:
    print("\n\n".join(failures), file=sys.stderr)
    sys.exit(2)  # non-zero -> Claude receives this output and can correct it

sys.exit(0)
