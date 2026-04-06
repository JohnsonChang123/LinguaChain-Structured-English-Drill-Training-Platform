import re
from dataclasses import dataclass
from typing import Any


def normalize_text(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[.!?]+$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


@dataclass
class EvaluationResult:
    is_correct: bool
    score: float
    feedback: dict[str, Any]


def evaluate_answer(user_input: str, target_answer: str) -> EvaluationResult:
    normalized_input = normalize_text(user_input)
    normalized_target = normalize_text(target_answer)

    is_correct = normalized_input == normalized_target
    score = 1.0 if is_correct else 0.0

    return EvaluationResult(
        is_correct=is_correct,
        score=score,
        feedback={
            "expected": target_answer,
            "normalized_input": normalized_input,
            "normalized_target": normalized_target,
            "error_type": None if is_correct else "mismatch",
        },
    )
