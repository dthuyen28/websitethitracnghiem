import json
import os
from utils.file_handler import load_json, save_json

EXAM_FILE = 'data/exams.json'


def load_exams():
    if not os.path.exists(EXAM_FILE):
        return {"exams": []}

    with open(EXAM_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, dict):
        return {"exams": []}

    return data


def save_exams(data):
    with open(EXAM_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_all_exams():
    data = load_exams()
    return data.get("exams", [])


def get_exam_by_id(exam_id):
    for e in get_all_exams():
        if e["id"] == exam_id:
            return e
    return None


def create_exam(title, subject, topic, source_type, question_ids):
    data = load_exams()
    exams = data["exams"]

    exam_id = max([e["id"] for e in exams], default=0) + 1

    new_exam = {
        "id": exam_id,
        "title": title,
        "subject": subject,
        "topic": topic,
        "source_type": source_type,
        "question_ids": question_ids,
        "num_questions": len(question_ids),

        # cấu hình mặc định
        "duration": 60,
        "shuffle": False,
        "show_result": True,

        # trạng thái
        "status": "closed"
    }

    exams.append(new_exam)
    save_exams(data)
    return new_exam

