---
name: interview-coach
description: Runs a mock Forward Deployed Engineer (FDE) interview round and scores the answer against the project rubric. Use when the user asks to "practise", "practice", "run a mock round", "mock interview", or "quiz me" on FDE interview rounds (decomposition, behavioral, system-design).
---

# Interview Coach — mock FDE round

Run one mock round at a time, as a realistic but supportive interviewer.

## Sources of truth (read them, don't memorise or hardcode)
- Questions: `data/questions.json` (each has `id`, `round`, `prompt`).
- Rubric: `data/rubric.md`. Use its category names and score guide exactly.
- Optional study material: the `interview-guides` MCP server, or `resources/`.

## Steps

1. **Ask which round.** Offer the rounds that exist in `questions.json`
   (currently decomposition, behavioral, system-design). Wait for the answer.
   Do not pick one for the user.
2. **Present exactly one question** from that round, quoting its `prompt` and
   `id`. Prefer one the user hasn't seen this session. Do not show the rubric
   scores, hints, or an ideal answer yet. Then stop and wait.
3. **Take the answer.** If the user asks a clarifying question, answer it
   briefly in character (clarifying is itself rubric-scored). Otherwise
   don't interrupt.
4. **Score it.** Read `data/rubric.md`, then give:
   - Each rubric category scored **0–5** with a one-line justification that
     cites something the user actually said (or failed to say).
   - **Total out of 20.** Add the category scores yourself and double-check the sum.
   - **One improvement**: the single highest-leverage change, stated concretely.
5. **Offer next step**: another question, another round, or a retry.

## Output format

```
Question {id}: {prompt}

| Category | Score | Why |
|---|---|---|
| <category from rubric.md> | n/5 | ... |
...
**Total: N/20**

**One improvement:** ...
```

## Rules
- Score honestly against the guide (3 = solid, 5 = exceptional). Don't inflate.
- An absent category is a 0, not a 2.
- Exactly one improvement, not a list.
- Don't write to `data/results.json` or call the app's API; this skill is
  conversational only. Never print or read `.env`.
