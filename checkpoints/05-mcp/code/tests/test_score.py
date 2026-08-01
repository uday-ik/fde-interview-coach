"""Scoring tests — written in Module 3.

The first test is the important one: against the START state's buggy
compute_total() it FAILS (the first category is dropped), which is exactly how
you discover the bug. Against the fixed version it passes.
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from app import scoring
from app.main import app
from app.models import CategoryScore

client = TestClient(app)


def test_compute_total_sums_every_category() -> None:
    """4 categories x 3 points = 12. The buggy version returns 9."""
    cats = [CategoryScore(name=n, score=3, feedback="") for n in scoring.RUBRIC_CATEGORIES]
    assert scoring.compute_total(cats) == 12


def test_score_endpoint_total_equals_sum_of_categories() -> None:
    """The headline invariant: the total must equal the sum of its parts."""
    resp = client.post(
        "/score",
        json={"round": "decomposition", "question_id": "dec-01", "answer": "line\n" * 6},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] == sum(c["score"] for c in body["categories"])


def test_scores_stay_within_bounds() -> None:
    """Every category score must sit inside the rubric's 0..5 range."""
    resp = client.post(
        "/score",
        json={"round": "behavioral", "question_id": "beh-01", "answer": "short"},
    )
    for category in resp.json()["categories"]:
        assert 0 <= category["score"] <= 5


def test_progress_endpoint_reports_attempts() -> None:
    """/progress should count the attempts recorded by /score."""
    resp = client.get("/progress")
    assert resp.status_code == 200
    body = resp.json()
    assert "rounds_practised" in body
    assert "average_total" in body
