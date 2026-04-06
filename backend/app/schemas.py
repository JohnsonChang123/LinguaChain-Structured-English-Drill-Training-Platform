from typing import Any

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CourseOut(BaseModel):
    id: int
    title: str
    cefr_level: str
    description: str


class LessonOut(BaseModel):
    id: int
    title: str
    transcript: str
    audio_url: str
    source_name: str
    source_url: str
    license_name: str
    license_url: str
    attribution_text: str


class DrillOut(BaseModel):
    id: int
    lesson_id: int
    drill_type: str
    prompt_text: str
    base_sentence: str
    target_answer: str
    metadata_json: dict[str, Any]
    sequence_order: int


class AttemptCreate(BaseModel):
    drill_id: int
    input_text: str


class AttemptResponse(BaseModel):
    is_correct: bool
    score: float
    feedback: dict[str, Any]


class ProgressLessonOut(BaseModel):
    lesson_id: int
    lesson_title: str
    completion_rate: float
    average_score: float


class ProgressResponse(BaseModel):
    items: list[ProgressLessonOut]
