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
from operator import and_

from werkzeug.utils import send_from_directory
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

    est = Estudio.query.all()

    estudios = (
        db.session.query(Estudio, Paciente).join(
            Estudio, Paciente.id == Estudio.paciente
        )
    ).all()

    flash(type(estudios))
    for estudio in estudios:
        flash(type(estudio[0]))
        flash(type(estudio[1]))

    return render_template("estudio/index.html", estudios=est)


def listar():
    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    return render_template("empleados/index.html")


def ver():
    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    return render_template("empleados/index.html")


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
    db.session.add(new_estudio)
    archivo = generar_factura(new_estudio)
    new_estudio.archivoPresupuesto = archivo
    db.session.commit()

    return redirect(url_for("estudio_estado1", estudio=new_estudio.id))


def estudio_estado1():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    ruta = current_app.config["UPLOADED_FACTURAS_DEST"]
    ruta_archivo = os.path.join(ruta, estudio.archivoPresupuesto)
    # ruta_archivo = "sdfsdf"
    return render_template(
        "estudio/estado1.html", estudio=estudio, ruta_archivo=estudio.archivoPresupuesto
    )


def estudio_estado1_carga():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    """if not check_permission(session["id"], "user_new"):
        abort(401)"""
    archivo = request.form["comprobante"]
    id_estudio = request.args.get("estudio")

    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()
    estudio.comprobanteDePago = archivo

    db.session.commit()
    #FALTA GUARDAR EL ARCHIVO Y AGREGAR EL BOTON DE DESCARGAR EL COMPROBANTE EXISTENTE
    return render_template("empleados/index.html")  # redirect


def download():
    filename = request.args.get("filename")
    ruta = current_app.config["UPLOADED_FACTURAS_DEST"]
    return send_from_directory(ruta, filename, environ=request.environ)

