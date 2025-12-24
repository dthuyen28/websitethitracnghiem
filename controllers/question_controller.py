from flask import Blueprint, render_template, request, redirect, url_for
from models.question_model import add_question, get_all_questions

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
