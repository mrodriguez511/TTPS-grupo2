from flask import (
    redirect,
    render_template,
    request,
    url_for,
    session,
    abort,
    flash,
    current_app,
)
from app.helpers.archivos import generar_factura
from app.models.estudio import Estudio
from app.models.user import User
from app.models.rol import Rol
import os

from app.models.punto_encuentro import (
    Paciente,
    MedicoDerivante,
    DiagnosticoPresuntivo,
    TipoEstudio,
)
from app.helpers.auth import authenticated
from app.db import db
from datetime import datetime

# import pdfkit

# Protected resources
def index():
    """listado de estudios"""

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    estudios = Estudio.query.all()  # ver consulta

    return render_template("empleados/index.html", estudios=estudios)


def new_estudio():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    pacientes = Paciente.query.all()
    medicos = MedicoDerivante.query.all()
    diagnoticos = DiagnosticoPresuntivo.query.all()
    tipos = TipoEstudio.query.all()

    return render_template(
        "estudio/alta.html",
        pacientes=pacientes,
        medicos=medicos,
        diagnosticos=diagnoticos,
        tipos=tipos,
    )


def create_estudio():
    """función para alta de estudio"""

    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    params = request.form

    new_estudio = Estudio(
        tipoEstudio=params["tipoEstudio"],
        medicoDerivante=params["medicoDerivante"],
        paciente=params["paciente"],
        empleado=session["id"],
        diagnosticoPresuntivo=params["diagnostico"],
        presupuesto=params["presupuesto"],
    )
    new_estudio.archivoPresupuesto = generar_factura(new_estudio)
   
    db.session.add(new_estudio)
    db.session.commit()

    return redirect(url_for("estudio_estado1"))


def estudio_estado1():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)
    estudio = "555"

    ruta = current_app.config["UPLOADED_FACTURAS_DEST"]
    ruta_archivo = os.path.join(ruta, "factura_" + str(estudio.id) + ".pdf")
    # factura = os.path.join(current_app.root_path, app.config["UPLOAD_FOLDER"])
    factura = "archivos/facturas/factura_" + "555" + ".pdf"
    return render_template("estudio/estado1.html", estudio=estudio, factura=factura)


def estudio_estado1_carga():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    """if not check_permission(session["id"], "user_new"):
        abort(401)"""

    return render_template("estudio/estado_1.html")
