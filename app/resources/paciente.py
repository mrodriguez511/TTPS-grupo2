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

    pacientes1 = (
        db.session.query(Paciente, ObraSocial)
        .filter(Paciente.obraSocial == ObraSocial.id)
        .all()
    )

    pacientes2 = Paciente.query.filter(Paciente.obraSocial == None).all()

    return render_template(
        "paciente/index.html", pacientes1=pacientes1, pacientes2=pacientes2
    )


def new_paciente():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    obrasSociales = ObraSocial.query.all()

    return render_template("estudio/alta_paciente.html", obrasSociales=obrasSociales)


def registrarPaciente():

    obrasSociales = ObraSocial.query.all()

    return render_template("paciente/registrar.html", obrasSociales=obrasSociales)


def registro_paciente():

    params = request.form
    paciente = Paciente.query.filter(Paciente.dni == params["dni"]).first()
    if paciente:
        flash("Ya existe un paciente con el DNI ingresado")
        return redirect(url_for("nuevoPaciente"))

    new_paciente = Paciente(
        params["nombre"],
        params["apellido"],
        params["dni"],
        params["fechaNacimiento"],
    )

    new_paciente.password = params["password"]

    if params["obraSocial"] != "0":
        new_paciente.obraSocial = params["obraSocial"]
        new_paciente.nroAfiliado = params["nroAfiliado"]

    if params["nombreTutor"] != "":
        new_paciente.nombre_tutor = params["nombreTutor"]
        new_paciente.apellido_tutor = params["apellidoTutor"]
        new_paciente.telefono = params["telefonoTutor"]
        new_paciente.direccion = params["direccionTutor"]
        new_paciente.email = params["emailTutor"]
        new_paciente.menor = True
    else:
        new_paciente.telefono = params["telefono"]
        new_paciente.direccion = params["direccion"]
        new_paciente.email = params["email"]
        new_paciente.menor = False

    db.session.add(new_paciente)
    db.session.commit()

    flash("Registro exitoso")
    return redirect(url_for("auth_loginPaciente"))


def create_paciente():

    """función para alta de paciente"""

    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    params = request.form
    paciente = Paciente.query.filter(
        or_(Paciente.dni == params["dni"], Paciente.email == params["email"])
    ).first()
    if paciente:
        flash("Ya existe un paciente con el DNI o email ingresado", "error")
        return redirect(url_for("paciente_new"))

    new_paciente = Paciente(
        params["nombre"],
        params["apellido"],
        params["dni"],
        params["fechaNacimiento"],
    )

    new_paciente.email = params["email"]
    new_paciente.telefono = params["telefono"]
    new_paciente.resumenHC = params["resumenHC"]
    new_paciente.password = params["dni"]

    if params["obraSocial"] != "0":
        new_paciente.obraSocial = params["obraSocial"]
        new_paciente.nroAfiliado = params["nroAfiliado"]

    db.session.add(new_paciente)
    db.session.commit()

    return redirect(url_for("paciente_index"))


def editar_paciente():

    """función para alta de paciente"""

    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2) and not (session["rol"] == 3):
        abort(401)

    paciente_id = request.args.get("id")
    paciente = Paciente.query.filter(Paciente.id == paciente_id).first()

    obrasSociales = ObraSocial.query.all()

    if session["rol"] == 2:
        return render_template(
            "paciente/editar_paciente.html",
            obrasSociales=obrasSociales,
            paciente=paciente,
        )
    else:
        return render_template(
            "paciente/editar_perfil.html",
            obrasSociales=obrasSociales,
            paciente=paciente,
        )


def update_paciente():

    """actualizar datos de paciente"""

    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    paciente_id = request.args.get("id")
    paciente = Paciente.query.filter(Paciente.id == paciente_id).first()

    params = request.form
    paciente.nombre = params["nombre"]
    paciente.apellido = params["apellido"]
    paciente.fechaNacimiento = params["fechaNacimiento"]
    paciente.telefono = params["telefono"]
    paciente.resumenHC = params["resumenHC"]

    if params["obraSocial"] != "0":
        paciente.obraSocial = params["obraSocial"]
        paciente.nroAfiliado = params["nroAfiliado"]
    else:
        paciente.obraSocial = None
        paciente.nroAfiliado = None

    db.session.commit()

    return redirect(url_for("paciente_index"))


def update_perfil():

    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 3):
        abort(401)

    paciente_id = session["id"]
    paciente = Paciente.query.filter(Paciente.id == paciente_id).first()

    params = request.form
    paciente.nombre = params["nombre"]
    paciente.apellido = params["apellido"]
    paciente.fechaNacimiento = params["fechaNacimiento"]

    if params["obraSocial"] != "0":
        paciente.obraSocial = params["obraSocial"]
        paciente.nroAfiliado = params["nroAfiliado"]
    else:
        paciente.obraSocial = None
        paciente.nroAfiliado = None

    if params["nombreTutor"] != "":
        paciente.nombre_tutor = params["nombreTutor"]
        paciente.apellido_tutor = params["apellidoTutor"]
        paciente.telefono = params["telefonoTutor"]
        paciente.direccion = params["direccionTutor"]
        paciente.email = params["emailTutor"]
        paciente.menor = True
    else:
        paciente.telefono = params["telefono"]
        paciente.direccion = params["direccion"]
        paciente.email = params["email"]
        paciente.menor = False

    db.session.commit()

    return redirect(url_for("paciente_home"))
