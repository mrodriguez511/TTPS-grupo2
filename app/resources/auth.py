from flask import redirect, render_template, request, url_for, abort, session, flash
from app.helpers.auth import authenticated
from app.models.user import User
from app.models.rol import Rol
from app.models.configuracion import Configuracion
from app.models.paciente import Paciente
from app.db import db
from operator import and_


def login():
    return render_template("auth/login.html")


def loginPaciente():
    return render_template("auth/loginPaciente.html")


def home():
    if not authenticated(session):
        return render_template("home.html")

    if session["rol"] == 1:
        return redirect(url_for("empleado_index"))

    if session["rol"] == 3:
        return redirect(url_for("paciente_home"))

    return redirect(url_for("empleado_home"))


def authenticate():

    params = request.form
    user = User.query.filter(
        User.email == params["email"] and User.password == params["password"]
    ).first()
    # le pido la primer tupla que machee

    if not user:
        flash("Usuario o clave incorrecto.", "error")
        return redirect(url_for("auth_login"))

    u = User.query.filter(User.email == params["email"]).first()

    if u and u.password != params["password"]:
        u.intentos += 1
        db.session.commit()
        if u.intentos <= 2:
            flash("Usuario o clave incorrecto.", "error")
            return redirect(url_for("auth_login"))
        else:
            u.activo = False
            db.session.commit()
            flash("Usuario Bloqueado", "error")
            return redirect(url_for("auth_login"))

    if not user.activo:
        flash("Usuario bloqueado.")
        return redirect(url_for("auth_login"))

    session["rol"] = user.rol
    session["email"] = user.email
    session["id"] = user.id
    session["pacObligado"] = (Configuracion.query.first()).pacienteObligado
    user.intentos = 0
    db.session.commit()
    flash("La sesión se inició correctamente.", "success")

    if user.rol == 1:
        return redirect(url_for("empleado_index"))

    if user.rol == 4:
        return redirect(url_for("configurador_home"))
    # return redirect(url_for("estudio_index"))
    return redirect(url_for("empleado_home"))


def authenticatePaciente():

    params = request.form
    pac = Paciente.query.filter(
        and_(Paciente.dni == params["dni"], Paciente.password == params["password"])
    ).first()

    # le pido la primer tupla que machee
    if not pac:
        flash("Usuario o clave incorrecto.", "error")
        return redirect(url_for("auth_loginPaciente"))

    session["rol"] = 3
    session["dni"] = pac.dni
    session["id"] = pac.id
    db.session.commit()
    flash("La sesión se inició correctamente.", "success")

    return redirect(url_for("paciente_home"))


def logout():
    del session["rol"]
    del session["id"]
    session.clear()
    flash("La sesión se cerró correctamente.", "success")

    return redirect(url_for("home"))
