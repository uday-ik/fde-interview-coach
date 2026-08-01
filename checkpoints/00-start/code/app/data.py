"""Load the question bank and rubric, and read/write results.

All disk access lives here, so the rest of the app never touches JSON files
directly. If storage ever moved to a database, this is the only file to change.
"""
from __future__ import annotations

import json

from .config import DATA_DIR
from .models import Question


def load_rounds() -> list[str]:
    """Return the available round types, derived from the question bank."""
    questions = load_questions()
    # dict.fromkeys keeps first-seen order and drops duplicates.
    return list(dict.fromkeys(q.round for q in questions))


def load_questions(round: str | None = None) -> list[Question]:
    """Load all questions, optionally filtered to a single round."""
    raw = json.loads((DATA_DIR / "questions.json").read_text(encoding="utf-8"))
    questions = [Question(**item) for item in raw]
    if round is not None:
        questions = [q for q in questions if q.round == round]
    return questions


def load_rubric() -> str:
    """Return the scoring rubric as markdown text."""
    return (DATA_DIR / "rubric.md").read_text(encoding="utf-8")


def save_result(record: dict) -> None:
    """Append one scored result to data/results.json."""
    path = DATA_DIR / "results.json"
    results = json.loads(path.read_text(encoding="utf-8"))
    results.append(record)
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
