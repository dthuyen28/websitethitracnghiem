from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template, session
from models.exam_result_model import (
    save_exam_result,
    save_temp_exam_result
)
from models.exam_model import get_exam_by_id
from models.question_model import get_all_questions
from datetime import datetime

result_bp = Blueprint(
    "result",
    __name__,
    url_prefix="/result"
)
@result_bp.route("/save-temp/<int:exam_id>", methods=["POST"])
def save_temp_result(exam_id):
    """
    Lưu kết quả tạm thời khi đang làm bài
    """
    data = request.get_json()

    answers = data.get("answers", {})
    user_email = data.get("user_email") 

    result = {
        "exam_id": exam_id,
        "answers": answers,
        "user_email": user_email
    }

    save_temp_exam_result(result)

    return jsonify({
        "status": "success",
        "message": "Đã lưu tạm bài làm"
    })
@result_bp.route("/submit/<int:exam_id>", methods=["POST"])
def submit_result(exam_id):
    user = session.get("user")
    if not user:
        flash("Bạn chưa đăng nhập!")
        return redirect(url_for("auth.login"))
    exam = get_exam_by_id(exam_id)
    if not exam:
        flash("Không tìm thấy bài thi!")
        return redirect(url_for("exam.exam_session_list"))

    question_ids = exam.get("question_ids", [])
    all_questions = get_all_questions()

    correct_map = {
        q["id"]: q["correct"]
        for q in all_questions
        if q["id"] in question_ids
    }

    answers = {}
    for key, value in request.form.items():
        if key.startswith("q"):
            q_id = int(key.replace("q", ""))
            answers[q_id] = value

    score = 0
    for q_id, correct in correct_map.items():
        if answers.get(q_id) == correct:
            score += 1

    total = len(correct_map)

    result = {
    "exam_id": exam_id,
    "student_name": user["name"],
    "student_email": user["email"],
    "answers": answers,
    "score": score,
    "total": total,
    "submitted_at": datetime.now().isoformat(),
    "status": "submitted"
    }

    save_exam_result(result)

    return render_template(
        "exam_result.html",
        exam=exam,
        score=score,
        total=total
    )
@result_bp.route("/view/<int:exam_id>")
def view_result(exam_id):
    user = session.get("user")
    if not user:
        flash("Bạn chưa đăng nhập!")
        return redirect(url_for("auth.login"))

    from models.exam_result_model import get_results_by_exam_and_student

    results = get_results_by_exam_and_student(
        exam_id=exam_id,
        email=user["email"]
    )

    if not results:
        flash("Chưa có kết quả!")
        return redirect(url_for("exam.exam_session_list"))

    return render_template(
        "exam_result.html",
        result=results[-1]  
    )
@result_bp.route("/admin/exam/<int:exam_id>")
def admin_view_exam_results(exam_id):
    from models.exam_result_model import get_results_by_exam
    from models.exam_model import get_exam_by_id

    exam = get_exam_by_id(exam_id)
    if not exam:
        flash("Không tìm thấy bài thi!")
        return redirect(url_for("exam.exam_list"))

    results = get_results_by_exam(exam_id)

    return render_template(
        "admin_exam_results.html",
        exam=exam,
        results=results
    )
