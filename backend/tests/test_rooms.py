from pathlib import Path

import pytest

from backend.app.engine import GameContent

CONTENT_DIR = Path(__file__).resolve().parents[2] / "content"

ROOM_FILES = list(CONTENT_DIR.glob("*.json"))


@pytest.mark.parametrize("room_file", ROOM_FILES)
def test_room_is_valid(room_file):
    GameContent.model_validate_json(
        room_file.read_text()
    )