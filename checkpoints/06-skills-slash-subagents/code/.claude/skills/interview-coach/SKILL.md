---
name: interview-coach
description: Run a mock FDE interview round and score the answer against the rubric. Use when the user asks to practise, run a mock round, or be scored on a Forward Deployed Engineer interview question.
---

# Interview Coach

A **Skill** packages a repeatable procedure so it runs the same way every time,
no matter who invokes it or how they phrase the request. This is how a Forward
Deployed Engineer codifies institutional knowledge — quality stops depending on
whoever wrote today's prompt.

*(Claude decides to load this on its own, based on the `description` above —
that's what makes a Skill different from a slash command you trigger manually.)*

## Procedure

1. Ask which round the user wants: **decomposition**, **client-roleplay**,
   **behavioral**, or **system-design**. If they're unsure, suggest decomposition
   (it's the signature FDE round).
2. Fetch a question for that round — from `data/questions.json`, or from the
   `/questions` endpoint if the app is running.
3. Present **one** question and wait. Stay in the interviewer role. You may ask a
   single follow-up that pushes on their riskiest assumption.
4. Score the answer against `data/rubric.md`: 0–5 for each of the four
   categories, one line of feedback each, a total out of 20, and a one-line
   summary.
5. Finish with the single most valuable thing to improve next time.

## Rules
- Never reveal the scores until after they've answered.
- Be specific in feedback — quote what they said rather than giving generic advice.
