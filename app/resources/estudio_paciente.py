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

    render = "paciente_estudio_estado" + str(estudio.estadoActual)
    if estudio.estadoActual > 5 and estudio.estadoActual < 10:
        render = "paciente_estudio_estado5"

    return redirect(url_for(render, estudio=estudio.id))


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
    return redirect(url_for("paciente_estudio_estado1", estudio=estudio.id))


def estudio_estado2():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 3):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    if estudio.estadoActual < 2:
        flash("no puede acceder a un estado futuro")
        return redirect(url_for("home"))

    tipoEstudio = TipoEstudio.query.filter(
        TipoEstudio.id == estudio.tipoEstudio
    ).first()

    if estudio.estadoActual > 2:
        return render_template(
            "estudio_paciente/estado2.html",
            estudio=estudio,
            tipoEstudio=tipoEstudio,
            firmado=estudio.consentimientoFirmado,
        )

    return render_template(
        "estudio_paciente/estado2.html",
        estudio=estudio,
        tipoEstudio=tipoEstudio,
    )


def estudio_estado2_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 3):
        abort(401)

    archivo = request.files["file"]
    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()

    extension = archivo.filename.split(".")
    extension = extension[1]
    filename = "consentimiento" + str(id_estudio) + "." + extension

    uploader(archivo, filename)

    estudio.consentimientoFirmado = filename
    estudio.estadoActual += 1
    db.session.commit()
    cargarNuevoEstado(estudio)
    return redirect(url_for("paciente_estudio_estado3", estudio=estudio.id))


def estudio_estado3():
    """seleccion de turno"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 3):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    if estudio.estadoActual < 3:
        flash("no puede acceder a un estado futuro")
        return redirect(url_for("home"))

    turnos = db.session.query(Estudio.turno).filter(Estudio.turno != None).all()

    agendados = ""
    for turno in turnos:
        agendados = agendados + str(turno[0].strftime("%d/%m/%Y-%H:%M")) + ","

    return render_template(
        "estudio_paciente/estado3.html", estudio=estudio, agendados=agendados
    )


def estudio_estado3_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 3):
        abort(401)

    fecha = request.form["fecha"]
    hora = request.form["hora"]

    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()

    turno = fecha.replace("-", "/") + "-" + hora
    estudio.turno = datetime.strptime(turno, "%Y/%m/%d-%H:%M")
    estudio.estadoActual += 1
    # falta chekear turno disponible

    db.session.commit()
    cargarNuevoEstado(estudio)

    return redirect(url_for("paciente_estudio_estado4", estudio=estudio.id))


def estudio_estado4():
    """toma de muestra"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 3):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    if estudio.estadoActual < 4:
        flash("no puede acceder a un estado futuro")
        return redirect(url_for("home"))

    enfecha = estudio.fecha < datetime.now()

    return render_template(
        "estudio_paciente/estado4.html", estudio=estudio, enfecha=enfecha
    )


def cancelar_turno():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 3):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    estudio.turno = None
    estudio.estadoActual -= 1

    db.session.commit()
    cargarNuevoEstado(estudio)

    return redirect(url_for("paciente_estudio_estado3", estudio=estudio.id))


def estudio_estado5():
    """envio de mail"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 3):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    if estudio.estadoActual < 5:
        flash("no puede acceder a un estado futuro")
        return redirect(url_for("home"))

    # resultado = Resultado.query.filter(Resultado.id == estudio.resultado_id).first()
    medico = MedicoDerivante.query.filter(
        MedicoDerivante.id == estudio.medicoDerivante
    ).first()

    if estudio.estadoActual > 9:
        fecha_envio = Estado.query.filter(
            and_(Estado.estudio == estudio_id, Estado.numero == 9)
        ).one()
        return render_template(
            "estudio_paciente/estado5.html",
            estudio=estudio,
            # resultado=resultado,
            medico=medico,
            fecha=fecha_envio,
        )

    return render_template(
        "estudio_paciente/estado5.html",
        estudio=estudio,
        # resultado=resultado,
        medico=medico,
    )


def estudio_finalizado():

    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 3):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()
    resultado = Resultado.query.filter(Resultado.id == estudio.resultado_id).first()

    return render_template(
        "estudio_paciente/estadofin.html",
        estudio=estudio,
        resultado=resultado,
    )


def uploader(archivo, filename):
    path = current_app.config["UPLOADED_FACTURAS_DEST"].replace("\\", "/")
    ruta = path + "/" + filename
    archivo.save(ruta)
    return filename
