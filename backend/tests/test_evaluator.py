from app.services.evaluator import evaluate_answer, normalize_text


def test_normalize_text_rules():
    assert normalize_text("  Hello   WORLD!!! ") == "hello world"


def test_evaluate_answer_correct_after_normalization():
    result = evaluate_answer("  Is she a teacher?  ", "is she a teacher")
    assert result.is_correct is True
    assert result.score == 1.0
    assert result.feedback["error_type"] is None


def test_evaluate_answer_incorrect():
    result = evaluate_answer("she is a teacher", "she is not a teacher")
    assert result.is_correct is False
    assert result.score == 0.0
    assert result.feedback["error_type"] == "mismatch"
