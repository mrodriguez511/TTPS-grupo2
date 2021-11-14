import sqlalchemy
from sqlalchemy.sql.elements import Null
from operator import or_, and_
from sqlalchemy.sql.expression import null
from app.db import db
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.helpers.auth import authenticated
from app.models.estudio import Estudio


def index():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    reportes = [
        "cantidad de estudios por tipo",
        "demora en la entrega de estudios",
        "cantidad de estudios por mes del año",
    ]

    return render_template("reportes/index.html", reportes=reportes)


def cant_estudios_tipo():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)
    estudios = db.session.query(Estudio).all()
    dicc = {}
    for estudio in estudios:
        mes = estudio.fecha.month
        if not mes in dicc:
            dicc[mes] = 1
        else:
            dicc[mes] += 1

    return render_template("reportes/cant_estudios_tipo.html", dicc=dicc)
