from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.user import User
from app.models.rol import Rol
from app.db import db


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

    if user.borrado:
        flash("Usuario bloqueado.")
        return redirect(url_for("auth_login"))

    session["rol"] = user.rol
    session["id"] = user.id
    flash("La sesión se inició correctamente.")

    if user.rol == 1:
        return redirect(url_for("empleado_index"))

    return redirect(url_for("estudio_index"))


def logout():
    del session["rol"]
    del session["id"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))
