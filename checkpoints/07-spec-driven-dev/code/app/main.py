"""FastAPI app — FINISHED version.

What changed from the start state:
  * POST /score is wired to scoring.score_answer() and records each result
  * GET /progress added (planned in Module 2, built in Module 3; spec written later in Module 7)
"""
from __future__ import annotations

import json

from fastapi import FastAPI, HTTPException

from . import data, scoring
from .config import DATA_DIR
from .models import Question, ScoreRequest, ScoreResponse

app = FastAPI(title="FDE Interview Prep Assistant")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check — handy for confirming the server is up."""
    return {"status": "ok"}


@app.get("/rounds")
def get_rounds() -> list[str]:
    """List the available interview round types."""
    return data.load_rounds()


@app.get("/questions")
def get_questions(round: str) -> list[Question]:
    """Return the questions for one round, e.g. /questions?round=decomposition."""
    questions = data.load_questions(round=round)
    if not questions:
        raise HTTPException(status_code=404, detail=f"No questions for round '{round}'")
    return questions


@app.post("/score")
def post_score(request: ScoreRequest) -> ScoreResponse:
    """Score a candidate's answer against the rubric, and record the attempt."""
    result = scoring.score_answer(request.answer)
    data.save_result(
        {
            "round": request.round,
            "question_id": request.question_id,
            "total": result.total,
            "max": result.max,
        }
    )
    return result


@app.get("/progress")
def get_progress() -> dict[str, float | int]:
    """Session stats: how many rounds practised, and the average total score."""
    results = json.loads((DATA_DIR / "results.json").read_text(encoding="utf-8"))
    count = len(results)
    average = round(sum(r["total"] for r in results) / count, 1) if count else 0
    return {"rounds_practised": count, "average_total": average}
