from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Attempt, Drill, LessonProgress, User
from app.schemas import AttemptCreate, AttemptResponse
from app.services.evaluator import evaluate_answer

router = APIRouter(prefix="/api/v1/attempts", tags=["attempts"])


@router.post("", response_model=AttemptResponse)
def create_attempt(
    payload: AttemptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    drill = db.query(Drill).filter(Drill.id == payload.drill_id).first()
    if not drill:
        raise HTTPException(status_code=404, detail="Drill not found")

    result = evaluate_answer(payload.input_text, drill.target_answer)

    attempt = Attempt(
        user_id=current_user.id,
        drill_id=drill.id,
        input_text=payload.input_text,
        is_correct=result.is_correct,
        score=result.score,
        feedback_json=result.feedback,
    )
    db.add(attempt)
    db.flush()

    lesson_id = drill.lesson_id
    total_drills = db.query(func.count(Drill.id)).filter(Drill.lesson_id == lesson_id).scalar() or 0

    lesson_attempts = (
        db.query(Attempt)
        .join(Drill, Drill.id == Attempt.drill_id)
        .filter(Attempt.user_id == current_user.id, Drill.lesson_id == lesson_id)
        .all()
    )

    attempts_count = len(lesson_attempts)
    avg_score = sum(a.score for a in lesson_attempts) / attempts_count if attempts_count else 0.0
    completed_drills = len({a.drill_id for a in lesson_attempts if a.is_correct})
    completion_rate = (completed_drills / total_drills) if total_drills else 0.0

    progress = (
        db.query(LessonProgress)
        .filter(LessonProgress.user_id == current_user.id, LessonProgress.lesson_id == lesson_id)
        .first()
    )
    if progress is None:
        progress = LessonProgress(user_id=current_user.id, lesson_id=lesson_id)
        db.add(progress)

    progress.attempts_count = attempts_count
    progress.completed_drills = completed_drills
    progress.total_drills = total_drills
    progress.average_score = avg_score
    progress.completion_rate = completion_rate

    db.commit()

    return AttemptResponse(
        is_correct=result.is_correct,
        score=result.score,
        feedback=result.feedback,
    )
