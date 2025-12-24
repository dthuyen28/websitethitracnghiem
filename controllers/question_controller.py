from flask import Blueprint, render_template, request, redirect, url_for
from models.question_model import add_question, get_all_questions,update_question

question_bp = Blueprint(
    'question',
    __name__,
    url_prefix='/question'
)

@question_bp.route('/dashboard')
def dashboard():
    questions = get_all_questions()
    return render_template('dashboard.html', questions=questions)

@question_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        question = request.form.get('question')
        a = request.form.get('a')
        b = request.form.get('b')
        c = request.form.get('c')
        d = request.form.get('d')
        correct = request.form.get('correct')

        if not all([question, a, b, c, d, correct]):
            return render_template(
                "add_question.html",
                error="Vui lòng nhập đầy đủ dữ liệu"
            )

        # gọi model
        add_question(question, a, b, c, d, correct)

        return redirect(url_for('question.dashboard'))

    return render_template('add_question.html')
@question_bp.route('/edit/<int:q_id>', methods=['GET', 'POST'])
def edit(q_id):
    questions = get_all_questions()
    question = next((q for q in questions if q["id"] == q_id), None)

    if not question:
        return "Không tìm thấy câu hỏi", 404

    if request.method == 'POST':
        content = request.form.get('question')
        a = request.form.get('a')
        b = request.form.get('b')
        c = request.form.get('c')
        d = request.form.get('d')
        correct = request.form.get('correct')

        if not all([content, a, b, c, d, correct]):
            return render_template('edit_question.html', question=question, error="Vui lòng nhập đầy đủ dữ liệu")

        update_question(q_id, content, a, b, c, d, correct)
        return redirect(url_for('question.dashboard'))

    return render_template('edit_question.html', question=question)