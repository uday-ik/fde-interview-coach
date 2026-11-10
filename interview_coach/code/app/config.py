"""Central configuration — one place for every setting.

TWO DIFFERENT CREDENTIALS ARE INVOLVED IN THIS WORKSHOP. Don't mix them up:

  1. THIS APP calls **OpenAI** to score interview answers  -> OPENAI_API_KEY
  2. **Claude Code** (the AI coding agent you build this project WITH) is a
     separate tool that authenticates against **Anthropic**. An OpenAI key
     cannot run Claude Code.

Good news: the app runs fine with NO key at all — it falls back to a small
offline "mock" scorer, so setup is zero-friction and tests never cost anything.
"""
from __future__ import annotations

import os
from pathlib import Path

# Folder paths, relative to the coach/ project root (this file is coach/app/config.py).
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RESOURCES_DIR = BASE_DIR / "resources"

# Which OpenAI model scores answers. Kept as ONE constant so it's swappable in
# a single edit. gpt-4o-mini is cheap and plenty good for scoring.
MODEL_ID = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

# No key -> offline mock scorer (app still works, tests stay free and fast).
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
USE_MOCK = OPENAI_API_KEY == ""
