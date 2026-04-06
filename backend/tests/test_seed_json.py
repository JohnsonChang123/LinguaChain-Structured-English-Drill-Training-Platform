import json
from pathlib import Path


def test_seed_json_has_required_attribution_fields():
    seed_path = Path(__file__).resolve().parents[1] / "app" / "seed" / "lesson_001.json"
    payload = json.loads(seed_path.read_text())

    lesson = payload["lesson"]
    for key in [
        "title",
        "transcript",
        "audio_url",
        "source_name",
        "source_url",
        "license_name",
        "license_url",
        "attribution_text",
    ]:
        assert key in lesson and lesson[key] is not None

    assert len(payload["drills"]) == 4
