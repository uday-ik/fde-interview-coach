# CLAUDE.md — FDE Interview Prep Assistant

> Claude Code reads this file at the start of every session. It's how you onboard
> the agent to THIS project — the way a senior engineer briefs a new hire.
>
> 🚧 This is a **skeleton on purpose**. You complete the TODO sections in
> **Module 1**, after touring the codebase with Claude Code.

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
<!-- TODO (Module 1): one line per folder — app/, data/, resources/, tests/ -->

## Conventions
<!-- TODO (Module 1): the house rules, for example:
     - Type-hint everything; keep functions small and named for what they do.
     - All LLM prompts live as named constants in scoring.py, never inline.
     - Return structured JSON errors; never leak a stack trace to the client. -->

## Guardrails for you, the agent
<!-- TODO (Module 1): how the agent should behave, for example:
     - Show the plan before large changes, and the diff before applying.
     - Build in small steps: one feature -> run -> test -> commit.
     - Never commit .env or secrets. -->

## How to run
```
python -m venv .venv
.venv\Scripts\activate            # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload     # open http://127.0.0.1:8000/docs
pytest -q
```
