import sqlalchemy
from sqlalchemy.sql.elements import Null
from operator import or_, and_
from sqlalchemy.sql.expression import null
from app.db import db
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.helpers.auth import authenticated
from app.models.estudio import Estudio
from app.models.paciente import Paciente
from app.models.tipoEstudio import TipoEstudio
from app.models.estado import Estado


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


def boxPlot():

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    lista = []

    estudios = (
        Estudio.query.filter(
            and_(
                Estudio.fecha >= str(2021) + "-01-01",
                Estudio.fecha <= str(2021) + "-12-31",
            )
        )
        .filter(Estudio.estadoActual == 10)
        .all()
    )

    if estudios:

        for estudio in estudios:
            id = estudio.id
            estado = Estado.query.filter(
                and_(Estado.estudio == id, Estado.numero == 10)
            ).first()
            cantDias = (estado.fecha - estudio.turno).days
            lista.append(cantDias)

        lista.sort()

        total = len(lista)
        min = lista[0]
        max = lista[total - 1]
        posQ1 = total // 4
        q1 = lista[posQ1 - 1] + lista[posQ1] / 2
        posQ2 = total // 2
        q2 = lista[posQ2 - 1] + lista[posQ2] / 2
        posQ3 = 3 * total // 4
        q3 = lista[posQ3 - 1] + lista[posQ3] / 2

    else:
        min = 0
        max = 0
        q1 = 0
        q2 = 0
        q3 = 0

    return render_template(
        "reportes/boxplot.html", min=min, max=max, q1=q1, q2=q2, q3=q3
    )
