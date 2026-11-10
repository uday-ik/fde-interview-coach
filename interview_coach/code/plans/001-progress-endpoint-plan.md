# Plan: GET /progress endpoint

## Context
The app can't yet show a learner how they're doing. `data/results.json` is meant to hold
scored results, so `GET /progress` should read it and return how many rounds have been
practised and the average total score. Working dir: `interview_coach/code/`.

## 1. Files to change
- `app/models.py`: add `ProgressResponse(BaseModel)` with `rounds_practised: int` and
  `average_total: float`.
- `app/data.py`: add `load_results() -> list[dict]`, next to `save_result()`. Per CLAUDE.md,
  all disk access lives here. It reads `results.json`, and returns `[]` if the file is missing.
- `app/scoring.py`: add `compute_progress(results: list[dict]) -> ProgressResponse`.
  It is pure: count the records, average their `total`, and return 0 / 0.0 for an empty list.
  Putting it here keeps `main.py` free of business logic.
- `app/main.py`: add `@app.get("/progress")` that calls `data.load_results()`, then
  `scoring.compute_progress(...)`, and returns the response.
- `tests/test_progress.py` (new): tests for `compute_progress` and for the endpoint.
- Not changed: `config.py`, `results.json`, and the `/score` stub.

## 2. Order
1. Settle the record shape and the definition of "rounds practised" (see risks).
2. `ProgressResponse` in `models.py`.
3. Tests first, using a hand-built list of dicts: empty, one record, several, rounding.
4. `compute_progress` in `scoring.py` until the tests pass.
   **Empty-results guard:** if there are no records (empty list, or none with a `total`),
   return `rounds_practised=0, average_total=0.0` *before* dividing. Never compute
   `sum / len` on an empty list, so there is no ZeroDivisionError.
5. `load_results` in `data.py`.
6. The route in `main.py`, then the endpoint test with a temp data dir.
7. Run `pytest -q`, then hit `/progress` in `/docs`.

**Test note:** write one test for the endpoint itself (`GET /progress`), using the temp
data dir, that checks the empty case returns `{"rounds_practised": 0, "average_total": 0.0}`
with status 200. Never point it at the real `data/results.json`.

## 3. What could break or is easy to get wrong
- **Division by zero.** `results.json` starts as `[]`, so the average needs an empty guard.
  The empty case is the first thing a learner will hit.
- **Tests touching the real file.** `data.py` does `from .config import DATA_DIR`, so
  monkeypatching `app.config.DATA_DIR` does nothing. Patch `app.data.DATA_DIR` to a `tmp_path`
  instead, or tests will read and pollute the real `data/results.json`.
- **Missing or corrupt file.** `load_results` should tolerate a missing file. Decide whether
  invalid JSON gives a structured 500 (per CLAUDE.md, no stack traces to the client) or an error we let propagate.
- **Records missing `total`.** Use a deliberate rule (skip bad records or fail clearly) rather than a bare `r["total"]` KeyError.
- **Depends on the seeded bug.** `compute_total()` drops the first category, so any totals
  saved today are too low. `/progress` will faithfully average wrong numbers until that bug is fixed.
- **Float output.** Round the average (e.g. 2 dp) so the JSON is stable and testable.
- **Route/response typing.** Declare `-> ProgressResponse` like the other endpoints so
  `/docs` shows the schema.

## 4. Riskiest assumption
**That `results.json` records contain a `total` field at all.** Nothing writes results yet:
`POST /score` is a stub that never calls `save_result()`, and `save_result(record: dict)` has no
defined schema. I'd be coding against a record shape that doesn't exist. Mitigation: define the
record shape first (at minimum `round`, `question_id`, `total`, `max`, and the wiring in `/score`
that saves it), or explicitly scope this task to the shape we assume, and say so in the tests.

Related ambiguity: "rounds practised" could mean the number of scored answers (`len(results)`) or
the number of *distinct* round types (`decomposition`, ...). I'd default to `len(results)`
and confirm with you.

## Verification
- `pytest -q`: new tests pass and existing ones stay green.
- `uvicorn app.main:app --reload`, then `GET /progress` shows `{rounds_practised: 0, average_total: 0.0}` on the empty file.
- Put two hand-written records in a temp results file and confirm the count and average.
