from flask import Blueprint, render_template,request, redirect, url_for, flash, session
import pandas as pd
from models.question_model import get_all_questions, save_questions_from_excel,get_all_questions
from models.exam_model import get_all_exams,create_exam,get_exam_by_id, update_config, update_status, delete_exam
from models.exam_session_model import get_open_exams
from models.exam_result_model import save_exam_result, get_results_by_exam_and_student
from utils.decorators import admin_required
exam_bp = Blueprint(
    'exam',
    __name__,
    url_prefix='/exam',
    template_folder='../views'
)

@exam_bp.route('/')
def exam_list():
    exams = get_all_exams()
    return render_template('exam_list.html', exams=exams)

@exam_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def exam_create():
    if request.method == 'POST':
        title = request.form.get('title')
        subject = request.form.get('subject')
        topic = request.form.get('topic')
        source_type = request.form.get('source_type')

        if not title or not subject:
            flash("Tên đề thi và môn học là bắt buộc!")
            return redirect(request.url)

        question_ids = []

        if source_type == 'select':
            ids = request.form.getlist('question_ids')
            if not ids:
                flash("Bạn chưa chọn câu hỏi nào!")
                return redirect(request.url)

            question_ids = list(map(int, ids))


        elif source_type == 'excel':
            file = request.files.get('file_excel')
            if not file or file.filename == '':
                flash("Vui lòng chọn file Excel!")
                return redirect(request.url)

            try:
                df = pd.read_excel(file)

                question_ids = list(map(
                    int,
                    save_questions_from_excel(df.to_dict(orient='records'))
            ))

            except Exception as e:
                flash(f"Lỗi khi đọc file Excel: {e}")
                return redirect(request.url)

        create_exam(
            title=title,
            subject=subject,
            topic=topic,
            source_type=source_type,
            question_ids=question_ids
        )

        flash("🎉 Tạo đề thi thành công!")
        return redirect(url_for('exam.exam_list'))

    questions = get_all_questions()
    return render_template('exam_create.html', questions=questions)

@exam_bp.route('/config/<int:id>', methods=['GET', 'POST'])
@admin_required
def exam_config(id):
    exam = get_exam_by_id(id)
    if not exam:
        flash("Không tìm thấy đề thi!")
        return redirect(url_for('exam.exam_list'))
    all_questions = get_all_questions()
    questions = [q for q in all_questions if q['id'] in exam.get('question_ids', [])]


    if request.method == 'POST':
        try:
            duration = int(request.form.get('duration', 60))
            shuffle_questions = request.form.get('shuffle_questions') == 'on'
            show_result = request.form.get('show_result') == 'on'


            update_config(id, duration, shuffle_questions, show_result)
            flash("Cập nhật cấu hình thành công!")
        except ValueError:
            flash("Vui lòng nhập số hợp lệ!")


        return redirect(url_for('exam.exam_list'))


    return render_template('exam_config.html', exam=exam, questions=questions)

@exam_bp.route('/status/<int:id>/<status>')
@admin_required
def exam_status(id, status):
    if status not in ['open', 'closed']:
        flash("Trạng thái không hợp lệ!")
        return redirect(url_for('exam.exam_list'))
    exam = get_exam_by_id(id)
    if not exam:
        flash("Không tìm thấy đề thi!")
        return redirect(url_for('exam.exam_list'))
    update_status(id, status)
    if status == 'open':
        flash("🟢 Đề thi đã được MỞ!")
    else:
        flash("🔴 Đề thi đã được ĐÓNG!")

    return redirect(url_for('exam.exam_list'))

@exam_bp.route('/delete/<int:id>', methods=['POST'])
@admin_required
def exam_delete(id):
    exam = get_exam_by_id(id)
    if not exam:
        flash("Không tìm thấy đề thi!")
        return redirect(url_for('exam.exam_list'))

    try:
        delete_exam(id)
        flash("🗑️ Xóa đề thi thành công!")
    except Exception as e:
        flash(f"Lỗi khi xóa đề thi: {e}")


    return redirect(url_for('exam.exam_list'))
@exam_bp.route("/exams")
def open_exam_list():
    exams = get_open_exams()
    return render_template("exam_list.html", exams=exams)

@exam_bp.route("/open")
def exam_session_list():
    exams = get_open_exams()
    return render_template(
        "exam_session_list.html",
        exams=exams
    )

@exam_bp.route("/start/<int:id>")
def start_exam(id):
    exam = get_exam_by_id(id)

    if not exam:
        flash("Không tìm thấy bài thi!")
        return redirect(url_for("exam.exam_session_list"))

    if exam.get("status") != "open":
        flash("Bài thi đã đóng!")
        return redirect(url_for("exam.exam_session_list"))

    all_questions = get_all_questions()
    questions = [q for q in all_questions if q["id"] in exam["question_ids"]]

    if exam.get("shuffle_questions"):
        import random
        random.shuffle(questions)
    
    return render_template(
        "exam_do.html",
        exam=exam,
        questions=questions
    )
@exam_bp.route("/submit/<int:id>", methods=["POST"])
def submit_exam(id):
    exam = get_exam_by_id(id)
    if not exam:
        flash("Không tìm thấy bài thi!")
        return redirect(url_for("exam.exam_session_list"))
    user = session.get("user")
    if not user:
        flash("Bạn chưa đăng nhập!")
        return redirect(url_for("auth.login"))

    student_email = user["email"]

    question_ids = exam.get("question_ids", [])
    all_questions = get_all_questions()

    correct_map = {
        q["id"]: q["correct"]
        for q in all_questions
        if q["id"] in question_ids
    }

    answers = {}
    for key, value in request.form.items():
        question_id = int(key.replace("q", ""))
        answers[question_id] = value

    score = sum(
        1 for qid, correct in correct_map.items()
        if answers.get(qid) == correct
    )

    total = len(correct_map)

    result = {
        "exam_id": id,
        "exam_title": exam["title"],
        "student_email": student_email,
        "student_name": user.get("name", ""),
        "score": score,
        "total": total
    }

    return render_template(
        "exam_result.html",
        result=result
    )
    #return redirect(url_for("exam.exam_session_list"))
@exam_bp.route("/result/<int:exam_id>")
def view_my_result(exam_id):
    user = session.get("user")
    if not user:
        flash("Bạn chưa đăng nhập!")
        return redirect(url_for("auth.login"))

    student_email = user["email"]

    results = get_results_by_exam_and_student(exam_id, student_email)

    if not results:
        flash("Chưa có kết quả!")
        return redirect(url_for("exam.exam_session_list"))

    return render_template(
        "exam_result.html",
        result=results[0]
    )
