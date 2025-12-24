from flask import Flask, redirect, url_for, render_template
from controllers.auth_controller import auth_bp
from controllers.question_controller import question_bp
from models.question_model import get_all_questions

app = Flask(__name__, template_folder='views')
app.secret_key = 'secret_key'

app.register_blueprint(auth_bp)
app.register_blueprint(question_bp)


@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    questions = get_all_questions()
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)