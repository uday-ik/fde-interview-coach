"""Tests for the scoring logic.  Run:  pytest -q"""
from __future__ import annotations

import pytest

from app.models import CategoryScore
from app.scoring import RUBRIC_CATEGORIES, compute_total, format_scorecard


def test_compute_total_sums_all_categories() -> None:
    categories = [
        CategoryScore(name=name, score=3, feedback="")
        for name in RUBRIC_CATEGORIES
    ]
    assert len(categories) == 4
    assert compute_total(categories) == 12


@pytest.mark.parametrize(
    ("total", "summary"),
    [
        (0, "Needs significant work"),
        (4, "Needs significant work"),
        (5, "Needs work"),
        (9, "Needs work"),
        (10, "Solid, with gaps"),
        (15, "Solid, with gaps"),
        (16, "Strong answer"),
        (19, "Strong answer"),
        (20, "Strong answer - full marks"),
    ],
)
def test_format_scorecard_summary_bands(total: int, summary: str) -> None:
    card = format_scorecard([CategoryScore(name="x", score=total, feedback="")])
    assert card.total == total
    assert card.summary == summary


def test_format_scorecard_max_is_sum_of_category_maxes() -> None:
    categories = [CategoryScore(name=n, score=1, feedback="") for n in RUBRIC_CATEGORIES]
    assert format_scorecard(categories).max == 20
