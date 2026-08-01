# Tasks: session progress endpoint

*Module 7 output — the spec broken into small, independently testable steps.
The agent implements them one at a time; you verify each before moving on.*

- [ ] **T1** Add a `GET /progress` route in `app/main.py` that reads `data/results.json`.
- [ ] **T2** Compute `rounds_practised` (count) and `average_total` (mean, 1 dp).
- [ ] **T3** Handle the empty case — return zeros, never divide by zero.
- [ ] **T4** Add a test: score two answers, then assert the count and the average.
- [ ] **T5** Confirm `ruff` + `mypy` are clean, run `pytest`, then commit.

> Small tasks are the point: each one is reviewable on its own, and a failing
> task tells you exactly where things went wrong.
