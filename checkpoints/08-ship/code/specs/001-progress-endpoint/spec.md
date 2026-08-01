# Spec: session progress endpoint

*Produced in **Module 7 (Spec-Driven Development)**. The spec is the source
of truth — the agent implements against it, and you verify the result against it.*

## Why
Learners want to see whether they're actually improving across practice rounds.

## What (user-facing)
A new `GET /progress` endpoint reports, across every scored attempt so far:
- `rounds_practised` — how many answers have been scored
- `average_total` — the mean total score out of 20, rounded to 1 decimal place

## Acceptance criteria
1. With no results yet, returns `{"rounds_practised": 0, "average_total": 0}`.
2. After N scored answers, `rounds_practised == N`.
3. `average_total` equals the mean of those answers' totals, to 1 decimal.
4. Reads from `data/results.json`. No new dependencies.
5. `ruff` and `mypy` stay clean; `pytest` stays green.

## Out of scope
Per-category trends, charts, date filtering, authentication. Those are future specs.
