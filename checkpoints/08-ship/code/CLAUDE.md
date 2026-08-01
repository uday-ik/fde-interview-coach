# CLAUDE.md — FDE Interview Prep Assistant

> Claude Code reads this file at the start of every session. It's how you onboard
> the agent to THIS project — the way a senior engineer briefs a new hire.
> *(Completed in Module 1.)*

## What we're building
A small FastAPI app that runs mock Forward Deployed Engineer interviews and
scores the answers against a rubric. Favour **clarity over cleverness** — every
line should be explainable in an interview.

## Stack
- Python 3.11+, **FastAPI** (served by uvicorn), **Pydantic v2**
- Data: plain **JSON files** in `data/` — no database
- Scoring: an offline **mock** scorer, or the **OpenAI API** when a key is set
  (the model id lives in one constant, `app/config.MODEL_ID`)
- Tests: **pytest** — never call the network in a test

## Project layout
- `app/` — the application: `main.py` (routes), `models.py` (Pydantic schemas),
  `data.py` (JSON load/save), `scoring.py` (mock + OpenAI scorer), `config.py` (settings).
- `data/` — `questions.json` (question bank), `rubric.md` (scoring rubric),
  `results.json` (scored attempts).
- `resources/` — interview guides in markdown; also served by the MCP server.
- `tests/` — pytest suites.

## Conventions
- Type-hint everything; keep functions small and named for what they do.
- All LLM prompts live as named constants in `scoring.py` — never inline strings
  scattered across files.
- Return structured JSON errors with the right HTTP status; never leak a stack
  trace to the client.
- Load the rubric from `data/rubric.md` — don't duplicate its text in code.

## Guardrails for you, the agent
- Show me the plan before large changes, and the diff before applying.
- Build in small steps: one feature -> run it -> test it -> commit. Don't
  generate the whole app in one shot.
- If something fails, tell me the root cause and the smallest fix before making
  sweeping changes.
- Never commit `.env` or any secret (they're in `.gitignore`).
- Don't add dependencies without saying why.

## How to run
```
python -m venv .venv
.venv\Scripts\activate            # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload     # open http://127.0.0.1:8000/docs
pytest -q
```
