from flask import Blueprint, render_template, flash, redirect, url_for
from models.exam_model import get_exam_by_id
from models.exam_result_model import load_results
from utils.decorators import admin_required

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="../views"
)

@admin_bp.route("/results/<int:exam_id>")
@admin_required
def exam_results(exam_id):
    exam = get_exam_by_id(exam_id)
    if not exam:
        flash("Không tìm thấy đề thi!")
        return redirect(url_for("exam.exam_list"))

    # Lọc kết quả theo bài thi
    results = [
        r for r in load_results()
        if r["exam_id"] == exam_id and r["status"] == "submitted"
    ]

    return render_template(
        "admin_exam_results.html",
        exam=exam,
        results=results
    )
