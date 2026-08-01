"""PreToolUse hook — stop Claude Code from reading .env (your secrets).

How a hook works: Claude Code pipes the proposed tool call to this script as
JSON on stdin. Exit 0 = allow. Exit 2 = BLOCK, and whatever we print to stderr
is shown to Claude so it understands why and can adjust.

This is the difference between asking nicely in CLAUDE.md ("please don't read
.env") and *guaranteeing* it. Hooks are enforcement, not suggestion.
"""
import json
import sys

payload = json.load(sys.stdin)
file_path = (payload.get("tool_input") or {}).get("file_path", "")

# Block the real secrets file, but allow the committed .env.example template.
if ".env" in file_path and not file_path.endswith(".env.example"):
    print("Blocked: .env holds secrets (e.g. OPENAI_API_KEY) and must not be read.",
          file=sys.stderr)
    sys.exit(2)

sys.exit(0)
