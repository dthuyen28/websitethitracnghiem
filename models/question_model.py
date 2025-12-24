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
        "correct": correct
    }

    data["questions"].append(new_question)
    save_json(FILE, data)

def get_all_questions():
    data = load_json(FILE)
    return data.get("questions", [])
