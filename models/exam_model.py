import json
import os
from utils.file_handler import load_json, save_json

EXAM_FILE = 'data/exams.json'


def load_exams():
    if not os.path.exists(EXAM_FILE):
        return {"exams": [],"metadata": {}}

    with open(EXAM_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return {"exams": [], "metadata": {}}

    if not isinstance(data, dict):
        return {"exams": [],"metadata": {}}
    if "exams" not in data or not isinstance(data["exams"], list):
        data["exams"] = []
    if "metadata" not in data or not isinstance(data["metadata"], dict):
        data["metadata"] = {}

    return data

def save_exams(data):
    with open(EXAM_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_all_exams():
    data = load_exams()
    return load_exams()["exams"]


def get_exam_by_id(exam_id):
    for exam in get_all_exams():
        if exam["id"] == exam_id:
            return exam
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

def update_config(exam_id, duration=None, shuffle=None, show_result=None):
   
    data = load_exams()
    exams = data["exams"]

    for e in exams:
        if e["id"] == exam_id:
            if duration is not None:
                e["duration"] = duration
            if shuffle is not None:
                e["shuffle"] = shuffle
            if show_result is not None:
                e["show_result"] = show_result
            break
    else:
        return False  # không tìm thấy exam

    save_exams(data)
    return True

def update_status(exam_id, status):
    data = load_exams()
    for e in data["exams"]:
        if e["id"] == exam_id:
            e["status"] = status
            save_exams(data)
            return True
    return False
import json

def delete_exam(exam_id):
    data = load_json(EXAM_FILE)
    exams = data.get("exams", [])
    exams = [e for e in exams if e['id'] != exam_id]
    data['exams'] = exams
    save_json(EXAM_FILE, data)