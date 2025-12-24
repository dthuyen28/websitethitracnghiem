from flask import Blueprint, render_template, request, redirect, url_for, session
from models.user_model import check_login, is_email_exists, add_user

auth_bp = Blueprint("auth", __name__, template_folder='../views')

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        if is_email_exists(email):
            message = "Email đã tồn tại"
        else:
            add_user(fullname, email, password)
            return redirect("/login")

    return render_template("register.html", message=message)
