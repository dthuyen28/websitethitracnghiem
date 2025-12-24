from flask import Blueprint, render_template, request, redirect, url_for
from models.user_model import register_user

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
