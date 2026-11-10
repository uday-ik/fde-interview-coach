---
description: Summarise saved mock-interview results (rounds practised, average, weakest category, next focus)
allowed-tools: Read
---

Read `data/results.json` (a JSON list of saved scorecards) and report on it.

If the file is missing, or the list is empty, reply only:
"No results yet. Practise a round first (try: run a mock round)." Do not invent numbers.

Otherwise, compute from the records. Each record has a `total` (out of 20) and a
`categories` list whose items have `name` and `score` (0–5). If a record has no
`total`, sum its category scores. Skip malformed records and say how many you skipped.

Report, in this order:
1. **Rounds practised**: the number of records.
2. **Average total**: mean of the totals, as `X.X / 20` (one decimal).
3. **Weakest category**: the category name with the lowest average score across
   records, with that average as `X.X / 5`. Use the category names exactly as they
   appear in the data. On a tie, name all tied categories.
4. **Focus next**: one concrete thing to practise, tied to the weakest category
   and `data/rubric.md` (read it for what that category rewards). One sentence or
   two, not a list.

Keep it short. Do not modify any file.
