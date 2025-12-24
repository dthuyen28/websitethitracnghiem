from utils.file_handler import load_json, save_json

FILE = "data/questions.json"


def add_question(content, a, b, c, d, correct):
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

def update_question(q_id, content, a, b, c, d, correct):
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
