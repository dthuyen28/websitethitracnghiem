from flask import Flask, redirect, url_for, render_template
from controllers.auth_controller import auth_bp
from controllers.question_controller import question_bp
from models.question_model import get_all_questions
from controllers.exam_controller import exam_bp
from controllers.result_controller import result_bp
from controllers.admin_controller import admin_bp
import os

app = Flask(__name__, template_folder='views')
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")

app.register_blueprint(auth_bp)
app.register_blueprint(question_bp)
app.register_blueprint(exam_bp)
app.register_blueprint(result_bp)
app.register_blueprint(admin_bp)


@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    questions = get_all_questions()
    return render_template("dashboard.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)