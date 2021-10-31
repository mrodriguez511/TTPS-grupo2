from app.db import db
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.punto_encuentro import Paciente
from app.helpers.auth import authenticated


def new_paciente():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    """if not check_permission(session["id"], "user_new"):
        abort(401)"""

    return render_template("estudio/alta_paciente.html")


def create_paciente():

    """función para alta de paciente"""

    if not authenticated(session):
        abort(401)
    """if not check_permission(session["id"], "paciente_create"):
        abort(401)"""

    params = request.form
    paciente = Paciente.query.filter(
        Paciente.dni == params["dni"] or Paciente.email == params["email"]
    ).first()
    if paciente:
        flash("Ya existe un paciente con el DNI o email ingresado")
        return redirect(url_for("paciente_new"))

    new_paciente = Paciente(**request.form)

    db.session.add(new_paciente)
    db.session.commit()

    return redirect(url_for("estudio_new"))
