import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Course, Drill, Lesson


def run_seed(db: Session):
    seed_path = Path(__file__).parent / "seed" / "lesson_001.json"
    payload = json.loads(seed_path.read_text())

    existing = db.query(Lesson).filter(Lesson.title == payload["lesson"]["title"]).first()
    if existing:
        print("Seed already exists")
        return

    course = Course(**payload["course"])
    db.add(course)
    db.flush()

    lesson = Lesson(course_id=course.id, **payload["lesson"])
    db.add(lesson)
    db.flush()

    for drill_data in payload["drills"]:
        db.add(Drill(lesson_id=lesson.id, **drill_data))

    db.commit()
    print("Seed inserted")


if __name__ == "__main__":
    session = SessionLocal()
    try:
        run_seed(session)
    finally:
        session.close()
