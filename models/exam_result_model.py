import json
import os

RESULT_FILE = "data/results.json"

def save_exam_result(result):
    if not os.path.exists(RESULT_FILE):
        data = []
    else:
        with open(RESULT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    data.append(result)

    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
