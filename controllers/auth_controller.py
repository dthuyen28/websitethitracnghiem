from flask import Blueprint, render_template, request, redirect, url_for
from models.user_model import check_login

auth_bp = Blueprint(
    'auth',
    __name__,
    template_folder='../views'
)
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('fullname')   
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            return render_template(
                'register.html',
                message="Vui lòng nhập đầy đủ thông tin"
            )

        success = register_user(name, email, password)

        if success:
            return render_template(
                'register.html',
                message="Đăng ký thành công"
            )
        else:
            return render_template(
                'register.html',
                message="Email đã tồn tại"
            )

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = check_login(email, password)

        if user:
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Sai email hoặc mật khẩu")

    return render_template('login.html')
