from functools import wraps
from flask import session, redirect, url_for, flash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get("user")

        if not user:
            flash("Bạn chưa đăng nhập!")
            return redirect(url_for("auth.login"))

        if user.get("role") != "admin":
            flash("Bạn không có quyền truy cập trang này!")
            return redirect(url_for("exam.exam_session_list"))

        return f(*args, **kwargs)
    return decorated_function
