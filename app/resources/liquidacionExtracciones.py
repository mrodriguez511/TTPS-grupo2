from flask import redirect, render_template, session, abort, request, url_for
from sqlalchemy.sql.operators import and_
from app.models.estudio import Estudio
from app.models.paciente import Paciente
from app.models.tipoEstudio import TipoEstudio
from app.helpers.auth import authenticated
from app.db import db

# lista los estudios cuya Extraccion no se abono
# y el estado actual es Esperando retiro de muestra de Extracciones


def index():

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    estudios = (
        db.session.query(
            Estudio,
            Paciente,
            TipoEstudio,
        )
        .filter(and_(Estudio.estadoActual > 4, Estudio.extraccionAbonada == False))
        .filter(Estudio.paciente == Paciente.id)
        .filter(Estudio.tipoEstudio == TipoEstudio.id)
        .all()
    )

    return render_template("liquidacionExtracciones/index.html", estudios=estudios)


def abonar():
    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    estudios_id = request.form.getlist("check_liquidar")

    for estudio_id in estudios_id:
        estudio = Estudio.query.filter(Estudio.id == estudio_id).first()
        estudio.extraccionAbonada = True
    db.session.commit()

    return redirect(url_for("liquidacionExtracciones_index"))
