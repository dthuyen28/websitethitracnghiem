import json
import os
from datetime import datetime

RESULT_FILE = "data/results.json"
def save_temp_exam_result(result):
    """
    Lưu kết quả tạm thời khi đang làm bài
    """
    os.makedirs(os.path.dirname(RESULT_FILE), exist_ok=True)

    if not os.path.exists(RESULT_FILE):
        data = []
    else:
        with open(RESULT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    result["status"] = "in_progress"
    result["updated_at"] = datetime.now().isoformat()

    data.append(result)
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_exam_result(result):
    if not os.path.exists(RESULT_FILE):
        data = []
    else:
        with open(RESULT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    data.append(result)

    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def load_results():
    if not os.path.exists(RESULT_FILE):
        return []

    with open(RESULT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
def get_results_by_exam_and_student(exam_id, email):
    results = load_results()
    return [
        r for r in results
        if r["exam_id"] == exam_id
        and r["student_email"] == email
        and r["status"] == "submitted"
    ]
def get_results_by_exam(exam_id):
    results = load_results()
    return [
        r for r in results
        if r["exam_id"] == exam_id
        and r["status"] == "submitted"
    ]
