"""Basic tests.  Run:  pytest -q

These cover the endpoints that already work in the seed. In Module 3 (test)
you'll ADD adversarial tests for /score that reveal the compute_total() bug.
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_rounds_not_empty() -> None:
    resp = client.get("/rounds")
    assert resp.status_code == 200
    assert "decomposition" in resp.json()


def test_questions_for_round() -> None:
    resp = client.get("/questions", params={"round": "decomposition"})
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_questions_unknown_round_returns_404() -> None:
    resp = client.get("/questions", params={"round": "does-not-exist"})
    assert resp.status_code == 404
