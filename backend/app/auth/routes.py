from flask import Blueprint, request, render_template, redirect, url_for, flash, make_response
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
    get_jwt_identity
)
from app.models import User
from app import db
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            flash("Please fill all fields.", "danger")
            return render_template("register.html")

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or Email already exists.", "warning")
            return render_template("register.html")

        user = User(username=username, email=email)
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Database error: {e}", "danger")
            return render_template("register.html")

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
            resp = make_response(redirect(url_for("main.dashboard")))
            set_access_cookies(resp, access_token)
            return resp
        else:
            flash("Invalid username or password.", "danger")
            return render_template("login.html")

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    resp = make_response(redirect(url_for("auth.login")))
    unset_jwt_cookies(resp)
    flash("Logged out successfully.", "success")
    return resp
