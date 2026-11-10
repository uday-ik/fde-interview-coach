# Tasks: `GET /progress`

Spec: `specs/001-progress-endpoint/spec.md` · Plan: `plans/001-progress-endpoint-plan.md`

Each task is one small change with its own test and a clear "done" check. Do them in
order; each builds only on the ones above it. Run `pytest -q` after every task.

Status below reflects the current code (the endpoint already exists).

---

## T1. Response schema: `ProgressResponse`
- **File:** `app/models.py`
- **Change:** add `ProgressResponse(BaseModel)` with `rounds_practised: int`, `average_total: float`.
- **Test:** build one with valid values; check both fields round-trip.
- **Done when:** the model imports and validates. Covers: *what it returns*.
- **Status:** done.

## T2. Pure calculation, empty case first
- **File:** `app/scoring.py` (`compute_progress`), `tests/test_progress.py`
- **Change:** `compute_progress([])` returns `rounds_practised=0, average_total=0.0`,
  returned *before* any division.
- **Test:** `test_compute_progress_empty`.
- **Done when:** the empty test passes with no `ZeroDivisionError`. Covers: AC 1.
- **Status:** done.

## T3. Pure calculation, count and average
- **File:** `app/scoring.py`, `tests/test_progress.py`
- **Change:** for non-empty input, count records and average their `total`, rounded to
  `AVERAGE_DECIMALS` (named constant, no magic number).
- **Tests:** single record (12 gives 12.0); several records (14, 15, 14 gives 14.33).
- **Done when:** both pass. Covers: AC 2, 3.
- **Status:** done.

## T4. Ignore records without a `total`
- **File:** `app/scoring.py`, `tests/test_progress.py`
- **Change:** skip records missing `total`; they count toward neither field. A list where
  none have `total` behaves like the empty case.
- **Test:** `test_compute_progress_ignores_records_without_total` (plus a "none have total" case).
- **Done when:** both pass. Covers: AC 4.
- **Status:** done. The "none have total" case has no dedicated test; add one.

## T5. Disk read: `load_results`
- **File:** `app/data.py`
- **Change:** `load_results() -> list[dict]` reads `DATA_DIR / "results.json"`; returns `[]`
  if the file is missing. Read-only. Nothing else touches the file.
- **Test:** with a temp `DATA_DIR`, missing file gives `[]`; a written file is returned as-is.
- **Done when:** tests pass and `results.json` is never modified. Covers: AC 1 (missing file), 5.
- **Status:** done. Missing-file case is tested through the endpoint, not directly; a direct
  `load_results` test is optional.

## T6. Route wiring
- **File:** `app/main.py`
- **Change:** `GET /progress` returns `scoring.compute_progress(data.load_results())` and
  nothing else (no logic in the route).
- **Test:** endpoint test with a temp data dir (`monkeypatch` `data.DATA_DIR`): missing file
  gives `200` and `{"rounds_practised": 0, "average_total": 0.0}`; seeded file gives the
  expected count and average.
- **Done when:** both endpoint tests pass offline and never touch the real
  `data/results.json`. Covers: AC 1, 6, 7.
- **Status:** done.

## T7. Manual check
- **Change:** none (verification only).
- **Steps:** `uvicorn app.main:app --reload`, open `/docs`, call `GET /progress`.
- **Done when:** the empty case returns `{"rounds_practised": 0, "average_total": 0.0}`
  with the real (empty) `results.json`, and the file is unchanged afterwards (`git diff data/`).
- **Status:** not yet run.
