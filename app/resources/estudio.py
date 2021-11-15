from flask import redirect, render_template, request, url_for, session, abort, flash
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
<<<<<<< HEAD

=======
from operator import and_
from sqlalchemy.sql.elements import Null
>>>>>>> a9e2b96ea7e0fe3181fab6d1f9d39b926854017e

from werkzeug.utils import send_from_directory
from app.helpers.archivos import generar_factura
from app.models.estudio import Estudio
from app.models.user import User
from app.models.rol import Rol
import os
import csv
from datetime import datetime


"""from app.models.punto_encuentro import (
    Paciente,
    MedicoDerivante,
    DiagnosticoPresuntivo,
    TipoEstudio,
)"""
from app.models.diagnosticoPresuntivo import DiagnosticoPresuntivo
from app.models.paciente import Paciente
from app.models.tipoEstudio import TipoEstudio
from app.models.medicoDerivante import MedicoDerivante

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

    estudios = (
        db.session.query(Estudio, Paciente, TipoEstudio)
        .filter(Estudio.paciente == Paciente.id)
        .filter(Estudio.tipoEstudio == TipoEstudio.id)
        .all()
    )

    return render_template("estudio/index.html", estudios=estudios)


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
    new_estudio.archivoPresupuesto = generar_factura(new_estudio)

    db.session.add(new_estudio)
<<<<<<< HEAD
=======

    archivo = generar_factura(new_estudio)  # genero el estudio
    new_estudio.archivoPresupuesto = archivo
>>>>>>> a9e2b96ea7e0fe3181fab6d1f9d39b926854017e
    db.session.commit()

    return redirect(url_for("estudio_estado1"))


def estudio_estado1():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio = "555"
    estudio_id = estudio.__getattribute__  # cambio para que tome el id

    ruta = current_app.config["UPLOADED_FACTURAS_DEST"]
    # ruta_archivo = os.path.join(ruta, "factura_" + str(estudio.id) + ".pdf")
    ruta_archivo = os.path.join(ruta, "factura_" + str(estudio_id) + ".pdf")

    # factura = os.path.join(current_app.root_path, app.config["UPLOAD_FOLDER"])
    factura = "archivos/facturas/factura_" + "555" + ".pdf"
    return render_template("estudio/estado1.html", estudio=estudio, factura=factura)
    ruta_archivo = os.path.join(ruta, estudio.archivoPresupuesto)
    # ruta_archivo = "sdfsdf"
    return render_template(
        "estudio/estado1.html", estudio=estudio, ruta_archivo=estudio.archivoPresupuesto
    )


def estudio_estado1_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    archivo = request.form["comprobante"]
    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()
    estudio.comprobanteDePago = archivo
    estudio.estadoActual += 1

    # archivo = generar_factura(new_estudio) #genero el estudio
    # new_estudio.archivoPresupuesto = archivo
    # db.session.commit()

    db.session.commit()
    # FALTA GUARDAR EL ARCHIVO Y AGREGAR EL BOTON DE DESCARGAR EL COMPROBANTE EXISTENTE
    return redirect(url_for("estudio_estado2", estudio=estudio.id))


def estudio_estado2():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    tipoEstudio = TipoEstudio.query.filter(
        TipoEstudio.id == estudio.tipoEstudio
    ).first()

    # ruta = current_app.config["UPLOADED_FACTURAS_DEST"]
    # ruta_archivo = os.path.join(ruta, estudio.archivoConsentimiento)

    # ruta_archivo = "sdfsdf"
    return render_template(
        "estudio/estado2.html",
        estudio=estudio,
        tipoEstudio=tipoEstudio,
    )


def estudio_estado2_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    archivo = request.form["consentimiento"]
    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()
    estudio.consentimientoFirmado = archivo
    estudio.estadoActual += 1

    # archivo = generar_factura(new_estudio) #genero el estudio
    # new_estudio.archivoPresupuesto = archivo
    # db.session.commit()

    db.session.commit()
    # FALTA GUARDAR EL ARCHIVO Y AGREGAR EL BOTON DE DESCARGAR EL COMPROBANTE EXISTENTE
    return redirect(url_for("estudio_estado3", estudio=estudio.id))


def estudio_estado3():
    """seleccion de turno"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    agendados = []  # query que traiga todos los turnos agendados

    """with open("archivos/Patologias.csv") as data_set:
        reader = csv.reader(data_set)
        for fila in reader:
            flash(fila[0])
            flash(type(fila))
            db.session.add(DiagnosticoPresuntivo(nombre=fila))
    """
    # ruta = current_app.config["UPLOADED_FACTURAS_DEST"]
    # ruta_archivo = os.path.join(ruta, estudio.archivoConsentimiento)

    # ruta_archivo = "sdfsdf"
    return render_template("estudio/estado3.html", estudio=estudio, agendados=agendados)


def estudio_estado3_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    fecha = request.form["fecha"] 
    hora = request.form["hora"] 

    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()

    turno = fecha.replace("-", "/") + "-" + hora
    estudio.turno = datetime.strptime(turno, "%Y/%m/%d-%H:%M")
    estudio.estadoActual += 1
    #falta chekear turno disponible

    db.session.commit()
<<<<<<< HEAD
    # FALTA GUARDAR EL ARCHIVO Y AGREGAR EL BOTON DE DESCARGAR EL COMPROBANTE EXISTENTE
    return render_template("empleados/index.html")  # redirect
=======

    return redirect(url_for("estudio_estado4", estudio=estudio.id))


def estudio_estado4():
    """toma de muestra"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    enfecha = estudio.fecha < datetime.now()
    return render_template("estudio/estado4.html", estudio=estudio, enfecha=enfecha)


def cancelar_turno():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()
    estudio.turno = None
    estudio.estadoActual -= 1

    agendados = []  # query que traiga todos los turnos agendados
    db.session.commit()

    return render_template("estudio/estado3.html", estudio=estudio, agendados=agendados)


def estudio_estado4_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    archivo = request.form["consentimiento"]
    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()
    estudio.consentimientoFirmado = archivo
    estudio.estadoActual += 1

    # archivo = generar_factura(new_estudio) #genero el estudio
    # new_estudio.archivoPresupuesto = archivo
    # db.session.commit()

    db.session.commit()
    # FALTA GUARDAR EL ARCHIVO Y AGREGAR EL BOTON DE DESCARGAR EL COMPROBANTE EXISTENTE
    return redirect(url_for("estudio_estado3", estudio=estudio.id))
>>>>>>> a9e2b96ea7e0fe3181fab6d1f9d39b926854017e


def download():
    filename = request.args.get("filename")
    ruta = current_app.config["UPLOADED_FACTURAS_DEST"]
    return send_from_directory(ruta, filename, environ=request.environ)
<<<<<<< HEAD

    db.session.commit()
    # FALTA GUARDAR EL ARCHIVO Y AGREGAR EL BOTON DE DESCARGAR EL COMPROBANTE EXISTENTE
    return render_template("empleados/index.html")  # redirect
=======
>>>>>>> a9e2b96ea7e0fe3181fab6d1f9d39b926854017e
