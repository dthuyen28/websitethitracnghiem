# models/exam_session_model.py

from utils.file_handler import load_json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXAM_FILE = os.path.join(BASE_DIR, "..", "data", "exams.json")


def get_open_exams():
    """
    Lấy danh sách bài thi đang mở cho người học
    """
    data = load_json(EXAM_FILE)

    if not data or "exams" not in data:
        return []

    exams = data["exams"]

    return [e for e in exams if e.get("status") == "open"]