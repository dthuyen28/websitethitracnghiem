from flask import Blueprint, render_template,request, redirect, url_for, flash
import pandas as pd
from models.question_model import get_all_questions, save_questions_from_excel,get_all_questions
from models.exam_model import get_all_exams,create_exam,get_exam_by_id, update_config, update_status, delete_exam
from models.exam_session_model import get_open_exams
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
def exam_create():
    if request.method == 'POST':
        title = request.form.get('title')
        subject = request.form.get('subject')
        topic = request.form.get('topic')
        source_type = request.form.get('source_type')

        # validate bắt buộc
        if not title or not subject:
            flash("Tên đề thi và môn học là bắt buộc!")
            return redirect(request.url)

        question_ids = []


        # -------- CHỌN CÂU HỎI --------
        if source_type == 'select':
            ids = request.form.getlist('question_ids')
            if not ids:
                flash("Bạn chưa chọn câu hỏi nào!")
                return redirect(request.url)

            question_ids = list(map(int, ids))

        # -------- IMPORT EXCEL --------
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

        # -------- TẠO ĐỀ --------
        create_exam(
            title=title,
            subject=subject,
            topic=topic,
            source_type=source_type,
            question_ids=question_ids
        )

        flash("🎉 Tạo đề thi thành công!")
        return redirect(url_for('exam.exam_list'))

    # GET
    questions = get_all_questions()
    return render_template('exam_create.html', questions=questions)

@exam_bp.route('/config/<int:id>', methods=['GET', 'POST'])
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
def exam_delete(id):
    exam = get_exam_by_id(id)
    if not exam:
        flash("Không tìm thấy đề thi!")
        return redirect(url_for('exam.exam_list'))

    # Gọi hàm xóa trong model
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

# học sinh xem danh sách bài thi
@exam_bp.route("/open")
def exam_session_list():
    exams = get_open_exams()
    return render_template(
        "exam_session_list.html",
        exams=exams
    )
# học sinh vào làm bài thi
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