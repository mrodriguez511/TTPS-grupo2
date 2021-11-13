from flask import redirect, render_template, session, abort
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.operators import and_

from app.models.estudio import Estudio

from app.helpers.auth import authenticated
from app.db import db

# lista los estudios cuya Extraccion no se abono
# y el estado actual es Esperando retiro de muestra de Extracciones


def index():

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    """estudios = Estudio.query.filter(
        and_(Estudio.extraccionAbonada == False, Estudio.muestra_ml != null)
    ).all()"""

    estudios = Estudio.query.filter(
        and_(Estudio.extraccionAbonada == False, Estudio.estadoActual == 5)
    ).all()

    return render_template("liquidacionExtracciones/index.html", estudios=estudios)
