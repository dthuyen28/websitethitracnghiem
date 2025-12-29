from utils.file_handler import load_json, save_json
import random, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "..", "data", "questions.json")



def add_question(content, a, b, c, d, correct,subject=None, topic=None):
    data = load_json(FILE)

    # đảm bảo cấu trúc
    if not isinstance(data, dict):
        data = {"questions": []}

    if "questions" not in data:
        data["questions"] = []

    new_question = {
        "id": len(data["questions"]) + 1,
        "content": content,
        "answers": {
            "A": a,
            "B": b,
            "C": c,
            "D": d
        },
        "correct": correct,
        "subject": subject,   
        "topic": topic     
    }

    data["questions"].append(new_question)
    save_json(FILE, data)

def get_all_questions():
    data = load_json(FILE)
    return data.get("questions", [])

def update_question(q_id, content, a, b, c, d, correct,subject=None, topic=None):
    data = load_json(FILE)
    questions = data.get("questions", [])
    for q in questions:
        if q["id"] == q_id:
            q["content"] = content
            q["answers"] = {"A": a, "B": b, "C": c, "D": d}
            q["subject"] = subject
            q["topic"] = topic
            q["correct"] = correct
            save_json(FILE, data)
            return True
    return False

def delete_question(q_id):
    data = load_json(FILE)
    questions = data.get("questions", [])
    questions = [q for q in questions if q["id"] != q_id]  # loại bỏ câu hỏi theo id
   
    for index, q in enumerate(questions, start=1):
        q["id"] = index
    data["questions"] = questions
    save_json(FILE, data)
    return True

def filter_questions(keyword="", subject="", topic=""):
    questions = get_all_questions()
    if keyword:
        questions = [q for q in questions if keyword.lower() in q["content"].lower()]
    if subject:
        questions = [q for q in questions if q.get("subject") and subject.lower() in q["subject"].lower()]
    if topic:
        questions = [q for q in questions if q.get("topic") and topic.lower() in q["topic"].lower()]
    return questions
# Đề thi
def get_questions_by_ids(ids):
    """
    Lấy danh sách câu hỏi theo danh sách ID
    """
    data = load_json(FILE)
    questions = data.get("questions", [])

    id_set = set(ids)
    return [q for q in questions if q.get("id") in id_set]

def get_random_question_ids(subject=None, num_questions=0, topic=None):
    """
    Lấy ngẫu nhiên ID câu hỏi theo môn học / chủ đề
    """

    questions = get_all_questions()

    # Lọc theo môn học
    if subject:
        questions = [
            q for q in questions
            if q.get("subject", "").lower() == subject.lower()
        ]

    # Lọc theo chủ đề (nếu có)
    if topic:
        questions = [
            q for q in questions
            if q.get("topic", "").lower() == topic.lower()
        ]

    # Không đủ câu hỏi
    if len(questions) < num_questions:
        return []

    random.shuffle(questions)
    return [q["id"] for q in questions[:num_questions]]
def save_questions_from_excel(rows):
    """
    Lưu danh sách câu hỏi từ file Excel
    rows: list[dict]
    """
    data = load_json(FILE)

    if "questions" not in data:
        data["questions"] = []

    questions = data["questions"]

    # ✅ ID an toàn
    start_id = max([q["id"] for q in questions], default=0) + 1
    new_ids = []

    for i, row in enumerate(rows):
        # 🔥 chuẩn hóa key (xóa khoảng trắng)
        row = {k.strip(): v for k, v in row.items()}

        content = row.get("content") or row.get("question")
        correct = row.get("correct")

        if not content or correct not in ["A", "B", "C", "D"]:
            continue

        q = {
            "id": start_id + i,
            "content": content,
            "answers": {
                "A": row.get("A"),
                "B": row.get("B"),
                "C": row.get("C"),
                "D": row.get("D"),
            },
            "correct": correct,
            "subject": row.get("subject"),
            "topic": row.get("topic"),
        }

        questions.append(q)
        new_ids.append(q["id"])

    save_json(FILE, data)
    return new_ids
