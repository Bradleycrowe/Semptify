# filepath: d:\Semptify\Semptify\register.py
from flask import Blueprint, render_template, request
from security import _get_or_create_csrf_token, save_user_token
register_bp = Blueprint("register", __name__, template_folder="templates")

@register_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", csrf_token=_get_or_create_csrf_token())
    token = save_user_token()
    return render_template("register_success.html", token=token)

