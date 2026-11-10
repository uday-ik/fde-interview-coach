# Spec 001: `GET /progress`

Plan: `plans/001-progress-endpoint-plan.md`

## Why
A learner practising mock rounds has no way to see how they're doing. Scored
results are saved to `data/results.json`, but nothing reads them back. `/progress`
gives a one-call answer to "how much have I practised, and how well am I scoring?"

## What it returns
`200 OK` with JSON matching `ProgressResponse`:

```json
{ "rounds_practised": 3, "average_total": 14.33 }
```

| Field | Type | Meaning |
|---|---|---|
| `rounds_practised` | int | Number of saved results that have a `total` |
| `average_total` | float | Mean of those totals (out of 20), rounded to `AVERAGE_DECIMALS` (2) |

## Acceptance criteria
1. **Empty case:** with no saved results (`[]`, or the file missing), returns `200`
   and `{"rounds_practised": 0, "average_total": 0.0}`. No error, no division by zero.
2. **One result** with `total: 12` returns `{"rounds_practised": 1, "average_total": 12.0}`.
3. **Several results** return the count and the mean of their totals, rounded to 2 decimals
   (e.g. totals 14, 15, 14 gives `14.33`).
4. **Records without a `total`** are ignored: they count toward neither field.
5. The endpoint is **read-only**: it never writes or modifies `results.json`.
6. The route holds no logic: `main.py` calls `data.load_results()` then
   `scoring.compute_progress(...)`.
7. Tests run offline and use a temp data dir, never the real `data/results.json`.

## What it reads
- `data/results.json`, a JSON list of scored result records, each with at least a
  `total`. Read only through `data.load_results()` (all disk access lives in `data.py`).

## Out of scope
- Per-category averages or the weakest category (the `/report` command covers that).
- Filtering by round, date or question; history or trend charts.
- Writing results: saving is `POST /score`'s job.
- Auth, per-user results, pagination, caching.
