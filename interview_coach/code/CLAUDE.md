# CLAUDE.md — FDE Interview Prep Assistant

## What we're building
A small FastAPI app that runs mock Forward Deployed Engineer interviews and
scores answers against a rubric (4 categories, each 0–5, max total 20). It's a
learning project: favour **clarity over cleverness**. Every line should be
explainable in an interview.

## Stack
- Python 3.11+, **FastAPI** (uvicorn), **Pydantic v2**
- Data: plain **JSON files** in `data/`. No database.
- Scoring: offline **mock** scorer by default, or the **OpenAI API** when
  `OPENAI_API_KEY` is set. The model id lives in one constant, `config.MODEL_ID`.
- Tests: **pytest**. Never call the network in a test.
- Note: the app uses an OpenAI key. Claude Code itself uses a separate Anthropic login.

## Project layout
- `app/main.py`: FastAPI routes only. No business logic.
- `app/models.py`: Pydantic request/response schemas.
- `app/scoring.py`: scoring logic (mock scorer, OpenAI scorer, totals, scorecard formatting).
- `app/data.py`: **all** disk access (questions, rubric, results). Nothing else touches JSON files.
- `app/config.py`: paths, `MODEL_ID`, `USE_MOCK`. All settings live here.
- `data/`: `questions.json`, `rubric.md`, `results.json`.
- `resources/`: study guides (STAR, decomposition, system design).
- `tests/`: pytest tests.

## Conventions
- Type-hint everything; keep functions small and named for what they do.
- Keep the rubric categories in one place (`RUBRIC_CATEGORIES` in `scoring.py`,
  mirrored by `data/rubric.md`). Don't hardcode category names elsewhere.
- All LLM prompts live as named constants in `scoring.py`, never inline.
- Read settings from `config.py`, never `os.environ` elsewhere. No hardcoded model ids.
- Validate at the edges with Pydantic; return structured JSON errors
  (`HTTPException`), never leak a stack trace to the client.
- No magic numbers or strings: name them as constants.

## Guardrails for you, the agent
- Show the plan before large changes, and the diff before applying.
- Build in small steps: one feature -> run -> test -> commit.
- When debugging, rank hypotheses *before* changing code.
- Refactor only with tests green before and after.
- Never read, print or commit `.env` or secrets. Update `.env.example` instead.
- Tests must work offline (force the mock scorer). Never spend API credits in tests.
- Don't add dependencies without asking.
- Commit only when asked.

## How to run
Run all commands from the `code/` folder. No API key is needed to start.

```
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload      # open http://127.0.0.1:8000/docs
pytest -q
```
