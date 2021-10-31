from flask import redirect, render_template, session, abort
from sqlalchemy.sql.expression import null
from app.models.punto_encuentro import Estudio
from app.helpers.auth import authenticated
from app.db import db


def index():

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    estudios = Estudio.query.filter(
        Estudio.extraccionAbonada == False, Estudio.muestra_ml == null
    ).all()

    return render_template("liquidacionExtracciones/index.html", estudios=estudios)
