from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Lesson, LessonProgress, User
from app.schemas import ProgressLessonOut, ProgressResponse

router = APIRouter(prefix="/api/v1/progress", tags=["progress"])


@router.get("/me", response_model=ProgressResponse)
def my_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = (
        db.query(LessonProgress, Lesson.title)
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .filter(LessonProgress.user_id == current_user.id)
        .order_by(LessonProgress.lesson_id.asc())
        .all()
    )

    items = [
        ProgressLessonOut(
            lesson_id=progress.lesson_id,
            lesson_title=title,
            completion_rate=progress.completion_rate,
            average_score=progress.average_score,
        )
        for progress, title in rows
    ]
    return ProgressResponse(items=items)
