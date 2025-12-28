from flask import Blueprint, render_template, request, redirect, url_for
from models.question_model import add_question, get_all_questions, update_question, delete_question
from utils.decorators import admin_required
question_bp = Blueprint(
    'question',
    __name__,
    url_prefix='/question'
)
@question_bp.route('/dashboard')
def dashboard():
    questions = get_all_questions()
    return render_template('dashboard.html', questions=questions)

@question_bp.route('/list')
def list_questions():
    subject = request.args.get('subject', '')
    topic = request.args.get('topic', '')
    keyword = request.args.get('q', '').lower()
    questions = get_all_questions()

    if subject:
        questions = [q for q in questions if q.get('subject','').lower() == subject.lower()]
    if topic:
        questions = [q for q in questions if q.get('topic','').lower() == topic.lower()]
    if keyword:
        questions = [q for q in questions if keyword in q['content'].lower()]

    return render_template('question_list.html', questions=questions)

@question_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add():
    if request.method == 'POST':
        question = request.form.get('question')
        a = request.form.get('a')
        b = request.form.get('b')
        c = request.form.get('c')
        d = request.form.get('d')
        correct = request.form.get('correct')
        subject = request.form.get('subject')  
        topic = request.form.get('topic') 

        if not all([question, a, b, c, d, correct]):
            return render_template("add_question.html", error="Vui lòng nhập đầy đủ dữ liệu")

        add_question(question, a, b, c, d, correct, subject, topic)
        # Sửa: Trả về đúng tên hàm list_questions
        return redirect(url_for('question.list_questions'))

    return render_template('add_question.html')

@question_bp.route('/edit/<int:q_id>', methods=['GET', 'POST'])
@admin_required
def edit(q_id):
    questions = get_all_questions()
    question = next((q for q in questions if q.get("id") == q_id), None)

    if not question:
        return f"Không tìm thấy câu hỏi với ID: {q_id}", 404

    if request.method == 'POST':
        content = request.form.get('question')
        a = request.form.get('a')
        b = request.form.get('b')
        c = request.form.get('c')
        d = request.form.get('d')
        correct = request.form.get('correct')
        subject = request.form.get('subject')
        topic = request.form.get('topic')

        if not all([content, a, b, c, d, correct]):
            return render_template('edit_question.html', question=question, error="Vui lòng nhập đầy đủ dữ liệu")

        update_question(q_id, content, a, b, c, d, correct, subject, topic)
        return redirect(url_for('question.list_questions'))

    return render_template('edit_question.html', question=question)

@question_bp.route('/delete/<int:q_id>', methods=['POST'])
@admin_required
def delete(q_id):
    delete_question(q_id)
    # Sửa: Tên hàm là list_questions chứ không phải list
    return redirect(url_for('question.list_questions'))