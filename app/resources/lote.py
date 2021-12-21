from flask import redirect, render_template, session, abort, request, url_for, flash
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.operators import and_
from app.helpers.estados import cargarNuevoEstado

from app.models.estudio import Estudio
from app.models.paciente import Paciente
from app.models.tipoEstudio import TipoEstudio
from app.models.lote import Lote
from operator import and_


from app.helpers.auth import authenticated
from app.db import db

# muestra todos los estudios cuyo estado actual es 6 (Esperando formar lote)
def estudiosFormarLote_index():

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    estudios = (
        db.session.query(Estudio, Paciente, TipoEstudio)
        .filter(Estudio.estadoActual == 6)
        .filter(Estudio.lote == None)
        .filter(Estudio.paciente == Paciente.id)
        .filter(Estudio.tipoEstudio == TipoEstudio.id)
        .all()
    )

    return render_template("lote/formarLote_index.html", estudios=estudios)


def formarLote():
    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)
    estudios_id = request.form["estudios"]
    estudios_id = estudios_id.split(",")

    lote = Lote()
    for estudio_id in estudios_id:
        estudio = Estudio.query.filter(Estudio.id == estudio_id).first()
        lote.estudios.append(estudio)

    db.session.add(lote)
    db.session.commit()

    for estudio_id in estudios_id:
        estudio = Estudio.query.filter(Estudio.id == estudio_id).first()
        estudio.estadoActual += 1
        db.session.commit()
        cargarNuevoEstado(estudio)

    flash("Lote creado exitosamente", "success")

    return redirect(url_for("estudiosFormarLote_index"))


def esperaURL_index():

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    lotes = Lote.query.filter(Lote.url == None).all()

    return render_template("lote/enProcesamiento.html", lotes=lotes)


def agregarURL():
    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    lote_id = request.args.get("id")
    url = request.form["url"]
    lote = Lote.query.filter(Lote.id == lote_id).first()
    lote.url = url

    db.session.commit()

    estudios_id = request.form.getlist("checkbox")
    for estudio_id in estudios_id:
        estudio = Estudio.query.filter(Estudio.id == estudio_id).first()
        estudio.estadoActual += 1
        db.session.commit()
        cargarNuevoEstado(estudio)

    for estudio in lote.estudios:
        if (
            estudio.estadoActual == 7
        ):  # si no avanzo de estado porque no fue tildado con el checkbox
            estudio.estadoActual = 3
            estudio.empleadoMuestra = None
            estudio.turno = None
            estudio.muestra_ml = None
            estudio.muestra_freezer = None
            estudio.lote = None
            db.session.commit()

    flash("URL ingresada exitosamente", "success")

    return redirect(url_for("lote_enProcesamiento_index"))


def procesados_index():
    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    lotes = Lote.query.filter(Lote.url != None).all()

    return render_template("lote/procesados.html", lotes=lotes)


def verEstudios():
    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    lote_id = request.args.get("id")

    estudios = (
        db.session.query(Estudio, TipoEstudio, Paciente)
        .filter(and_(Estudio.tipoEstudio == TipoEstudio.id, Estudio.lote == lote_id))
        .filter(Estudio.paciente == Paciente.id)
        .all()
    )
    # estudios = Estudio.query.filter(Estudio.lote == lote_id).all()

    return render_template("lote/verEstudios.html", estudios=estudios, lote=lote_id)
