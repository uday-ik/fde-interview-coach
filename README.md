# FDE Interview Prep Assistant

A tiny FastAPI app you build step by step with **Claude Code** — learning the tool as you
go (Plan Mode, testing, debugging, hooks, MCP, skills, spec-driven development). By the
end you have a working assistant that runs mock interviews and scores your answers.

> **Follow the demo guide.** This repo is just the code you work on during the session.
> The full step-by-step instructions live in the **FDE Interview Coach demo guide**
> provided with the course — keep it open beside you.

## Quick start
```
cp -r checkpoints/00-start/code my-coach     # Windows: xcopy /E /I checkpoints\00-start\code my-coach
cd my-coach
pip install -r requirements.txt
uvicorn app.main:app --reload                # open http://127.0.0.1:8000/docs
pytest -q
```

Each `checkpoints/<module>/code/` folder is a complete, runnable snapshot — if you fall
behind, copy that module's `code/` over your `my-coach/` and continue.

No API key needed to start — the app scores answers with an offline mock. (Claude Code
itself signs in separately, with your **Anthropic** account.)
