"""Tests for GET /progress.  Run:  pytest -q

The endpoint test points app.data.DATA_DIR at a temp folder so it never reads
or writes the real data/results.json. (data.py imports DATA_DIR by name, so it
must be patched on app.data, not app.config.)
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import data
from app.main import app
from app.scoring import compute_progress

client = TestClient(app)


def test_compute_progress_empty() -> None:
    result = compute_progress([])
    assert result.rounds_practised == 0
    assert result.average_total == 0.0


def test_compute_progress_single_record() -> None:
    result = compute_progress([{"total": 12}])
    assert result.rounds_practised == 1
    assert result.average_total == 12.0


def test_compute_progress_several_records_rounds_average() -> None:
    result = compute_progress([{"total": 10}, {"total": 11}, {"total": 11}])
    assert result.rounds_practised == 3
    assert result.average_total == 10.67


def test_compute_progress_ignores_records_without_total() -> None:
    result = compute_progress([{"total": 10}, {"round": "decomposition"}])
    assert result.rounds_practised == 1
    assert result.average_total == 10.0


def test_compute_progress_no_record_has_total_behaves_like_empty() -> None:
    result = compute_progress([{"round": "decomposition"}, {"round": "behavioral"}])
    assert result.rounds_practised == 0
    assert result.average_total == 0.0


@pytest.fixture
def temp_data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(data, "DATA_DIR", tmp_path)
    return tmp_path


def test_progress_endpoint_missing_file(temp_data_dir: Path) -> None:
    resp = client.get("/progress")
    assert resp.status_code == 200
    assert resp.json() == {"rounds_practised": 0, "average_total": 0.0}


def test_progress_endpoint_with_results(temp_data_dir: Path) -> None:
    (temp_data_dir / "results.json").write_text(
        json.dumps([{"total": 10}, {"total": 15}]), encoding="utf-8"
    )
    resp = client.get("/progress")
    assert resp.status_code == 200
    assert resp.json() == {"rounds_practised": 2, "average_total": 12.5}
