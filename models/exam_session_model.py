# models/exam_session_model.py

from utils.file_handler import load_json

EXAM_FILE = 'data/exams.json'

def get_open_exams():
    """
    Lấy danh sách bài thi đang mở cho người học
    """
    data = load_json(EXAM_FILE)

    if not data or "exams" not in data:
        return []

    exams = data["exams"]

    return [e for e in exams if e.get("status") == "open"]