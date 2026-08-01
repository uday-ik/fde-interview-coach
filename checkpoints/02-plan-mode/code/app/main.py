"""FastAPI app for the FDE Interview Prep Assistant.

Run it:
    uvicorn app.main:app --reload
Then open http://127.0.0.1:8000/docs  -- the interactive API page is our "UI".
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException

from . import data
from .models import CategoryScore, Question, ScoreRequest, ScoreResponse

app = FastAPI(title="FDE Interview Prep Assistant")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check."""
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
    """Score a candidate's answer against the rubric.

    STUB (Module 3 - build): right now this returns a fixed placeholder.
    During the workshop you'll wire it to scoring.score_answer(request.answer)
    so it returns real per-category scores and saves the result.
    """
    placeholder = [
        CategoryScore(name="Clarifying questions", score=0, feedback="not scored yet"),
    ]
    return ScoreResponse(
        total=0, max=5, categories=placeholder, summary="Scoring not implemented yet"
    )
