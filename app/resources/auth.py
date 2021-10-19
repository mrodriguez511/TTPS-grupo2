from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.user import User


def login():

    return render_template("auth/login.html")


def authenticate():

    params = request.form
    user = User.query.filter(
        User.email == params["email"] and User.password == params["password"]
    ).first()
    # le pido la primer tupla que machee

    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))

    if not user.activo:
        flash("Usuario bloqueado.")
        return redirect(url_for("auth_login"))

    session["user"] = user.email
    session["id"] = user.id
    flash("La sesión se inició correctamente.")

    return redirect(url_for("home"))


def logout():
    del session["user"]
    del session["id"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))
