# Plan: add a session progress endpoint

*Produced in **Module 2 (Plan Mode)** — Claude Code explored the codebase in
read-only mode and proposed this. Nothing was written until the plan was
approved. Store plans in the repo: they double as decision records and as
ready-made PR descriptions.*

## Goal
Let a learner see how they're improving across practice rounds.

## Files to touch
| File | Change |
|---|---|
| `app/main.py` | Add a `GET /progress` route |
| `tests/test_score.py` | Add a test covering the new route |

*(No new dependencies. `data/results.json` already stores every scored attempt.)*

## Order of work
1. Read `data/results.json` in the new route.
2. Return `rounds_practised` (count) and `average_total` (mean, 1 decimal).
3. Handle the empty case so there's no divide-by-zero.
4. Add the test, run the suite, commit.

## What could break
- `results.json` is empty on a fresh clone -> must return zeros, not crash.
- `save_result()` must have run at least once for the numbers to be meaningful,
  so `/score` needs to be working first.

## Riskiest assumption
That every record in `results.json` has a `total` key. If an older record
doesn't, the sum raises a `KeyError` — worth a defensive read or a test.
