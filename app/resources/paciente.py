import sqlalchemy
from sqlalchemy.sql.elements import Null
from operator import or_, and_

from sqlalchemy.sql.expression import null
from app.db import db
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.obraSocial import ObraSocial
from app.models.paciente import Paciente
from app.helpers.auth import authenticated


def index():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    """consulta = "select p.id, p.nombre, p.apellido, p.dni, p.telefono , o.nombre , p.nroAfiliado from pacientes as p left join obrassociales as o on p.obraSocial = o.id"
    pacientes = db.session.execute(consulta)

    p = pacientes.fetchall()"""

    prueba = (
        db.session.query(Paciente, ObraSocial)
        .filter(or_(Paciente.obraSocial == ObraSocial.id, Paciente.obraSocial == None))
        .all()
    )

    return render_template("paciente/index.html", pacientes=prueba)


def new_paciente():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    """if not check_permission(session["id"], "user_new"):
        abort(401)"""

    obrasSociales = ObraSocial.query.all()

    return render_template("estudio/alta_paciente.html", obrasSociales=obrasSociales)


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
