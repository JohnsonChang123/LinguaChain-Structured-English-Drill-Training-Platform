from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Drill, Lesson
from app.schemas import DrillOut, LessonOut

router = APIRouter(prefix="/api/v1/lessons", tags=["lessons"])


@router.get("/{lesson_id}", response_model=LessonOut)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.get("/{lesson_id}/drills", response_model=list[DrillOut])
def get_lesson_drills(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return (
        db.query(Drill)
        .filter(Drill.lesson_id == lesson_id)
        .order_by(Drill.sequence_order.asc())
        .all()
    )
