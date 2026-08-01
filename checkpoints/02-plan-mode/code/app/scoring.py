"""Scoring logic: turn a candidate's answer into a rubric-based scorecard.

>>> THIS FILE IS WHERE MOST OF THE WORKSHOP HAPPENS. <<<

In this START state, POST /score is not wired to any of it yet (see app/main.py).
During Module 3 you will, with Claude Code:
  * build    -> implement score_with_openai() and wire /score to score_answer()
  * test     -> write tests pinning  total == sum(category scores)
  * debug    -> those tests reveal the BUG in compute_total()      (marked below)
  * refactor -> clean up the messy format_scorecard()              (marked below)
"""
from __future__ import annotations

from .config import USE_MOCK
from .models import CategoryScore, ScoreResponse

# The four things every answer is scored on (mirrors data/rubric.md).
RUBRIC_CATEGORIES = [
    "Clarifying questions",
    "Decomposition",
    "Risk identification",
    "Communication",
]


def score_mock(answer: str) -> list[CategoryScore]:
    """A tiny deterministic scorer used when there is no OpenAI key.

    Intentionally simple: longer, more structured answers score a little higher.
    The workshop is about the *workflow*, not about building a clever scorer.
    """
    length_signal = min(len(answer) // 120, 5)  # 0..5 by answer length
    structure_signal = min(answer.count("\n") + 1, 5)  # 0..5 by line breaks
    base = max(1, (length_signal + structure_signal) // 2)
    return [
        CategoryScore(name=name, score=base, feedback=f"Auto-estimate for '{name}'.")
        for name in RUBRIC_CATEGORIES
    ]


def compute_total(categories: list[CategoryScore]) -> int:
    """Sum the per-category scores into a single total.

    *** SEEDED BUG — Module 3 (debug) ***
    This iterates over `categories[1:]`, so it silently DROPS the first category
    and every total comes out too low. It is left here on purpose: the tests you
    write should catch it, and you'll fix it with Claude Code by ranking
    hypotheses BEFORE changing any code.
    """
    total = 0
    for category in categories[1:]:  # BUG: should be `for category in categories`
        total += category.score
    return total


def format_scorecard(categories: list[CategoryScore]) -> ScoreResponse:
    """Assemble the final ScoreResponse from the category scores.

    *** UGLY FUNCTION — Module 3 (refactor) ***
    Deeply nested, repeats itself, and hides magic numbers/strings. It works,
    but you'll refactor it into something small and flat with Claude Code while
    keeping the tests green the whole way.
    """
    total = compute_total(categories)
    maximum = 0
    for c in categories:
        maximum = maximum + c.max
    if total >= 16:
        summary = "Strong answer"
        if total == 20:
            summary = "Strong answer - full marks"
        else:
            summary = "Strong answer"
    else:
        if total >= 10:
            summary = "Solid, with gaps"
        else:
            if total >= 5:
                summary = "Needs work"
            else:
                summary = "Needs significant work"
    return ScoreResponse(total=total, max=maximum, categories=categories, summary=summary)


def score_with_openai(answer: str) -> list[CategoryScore]:
    """Score using the real OpenAI API.

    *** STUB — Module 3 (build) ***
    Implement this to send the rubric (data/rubric.md) plus the candidate's
    answer to OpenAI using config.MODEL_ID, ask for JSON back, and parse it into
    one CategoryScore per rubric category. For now it just calls the mock so the
    app keeps working.
    """
    # TODO(workshop): call the OpenAI API here and parse the JSON response.
    return score_mock(answer)


def score_answer(answer: str) -> ScoreResponse:
    """Score one answer end to end (mock offline, OpenAI when a key is set)."""
    categories = score_with_openai(answer) if not USE_MOCK else score_mock(answer)
    return format_scorecard(categories)
