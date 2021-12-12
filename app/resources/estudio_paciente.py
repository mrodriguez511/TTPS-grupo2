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
import sqlalchemy
from sqlalchemy.sql.sqltypes import DateTime
from werkzeug.utils import send_from_directory
from werkzeug.utils import secure_filename
from app.helpers.archivos import generar_factura
from app.helpers.estados import cargarNuevoEstado
from app.models.estado import Estado
from app.models.estudio import Estudio
from app.models.estado import Estado
from app.models.medicoInformante import MedicoInformante
from app.models.user import User
from app.models.resultado import Resultado
from app.models.lote import Lote
from app.models.rol import Rol
import os
from datetime import date, datetime
from app.models.diagnosticoPresuntivo import DiagnosticoPresuntivo
from app.models.paciente import Paciente
from app.models.tipoEstudio import TipoEstudio
from app.models.medicoDerivante import MedicoDerivante
from app.helpers.auth import authenticated
from app.db import db
from datetime import datetime
from operator import and_


def misEstudios():
    """listado de estudios"""

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 3):
        abort(401)

    estudios = (
        db.session.query(Estudio, TipoEstudio)
        .filter(
            and_(
                Estudio.tipoEstudio == TipoEstudio.id, Estudio.paciente == session["id"]
            )
        )
        .all()
    )

    return render_template("paciente/home.html", estudios=estudios)


def ver():
    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 3):
        abort(401)

    estudio_id = request.args.get("id")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    return redirect(
        url_for(
            "paciente_estudio_estado" + str(estudio.estadoActual), estudio=estudio.id
        )
    )


def estudio_estado1():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 3):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    if estudio.estadoActual > 1:
        return render_template(
            "estudio_paciente/estado1.html",
            estudio=estudio,
            presupuesto=estudio.archivoPresupuesto,
            comprobante=estudio.comprobanteDePago,
        )

    return render_template(
        "estudio_paciente/estado1.html",
        estudio=estudio,
        filename=estudio.archivoPresupuesto,
    )


def estudio_estado1_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 3):
        abort(401)

    archivo = request.files["file"]
    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()

    # estudio.estadoActual += 1

    extension = archivo.filename.split(".")
    extension = extension[1]
    filename = "comprobante" + str(id_estudio) + "." + extension

    uploader(archivo, filename)

    estudio.comprobanteDePago = filename

    db.session.commit()
    cargarNuevoEstado(estudio)
    return redirect(url_for("paciente_estudio_estado1", estudio=estudio.id))


def uploader(archivo, filename):
    path = current_app.config["UPLOADED_FACTURAS_DEST"].replace("\\", "/")
    ruta = path + "/" + filename
    archivo.save(ruta)
    return filename
