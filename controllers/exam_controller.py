from flask import Blueprint, render_template,request, redirect, url_for, flash
import pandas as pd
from models.question_model import get_all_questions, save_questions_from_excel
from models.exam_model import get_all_exams,create_exam

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
