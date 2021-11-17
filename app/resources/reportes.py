from re import split
import sqlalchemy
from sqlalchemy.sql.elements import Null
from operator import or_, and_
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import DATE, DateTime
from app.db import db
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.helpers.auth import authenticated
from app.models.estudio import Estudio
from app.models.estado import Estado
from app.models.tipoEstudio import TipoEstudio
from datetime import date
from datetime import datetime
from sqlalchemy import func
from flask import flash


def cantTipo():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    tipos = (
        db.session.query(Estudio.tipoEstudio, func.count(Estudio.tipoEstudio))
        .group_by(Estudio.tipoEstudio)
        .all()
    )

    total_tipos = [0, 0, 0, 0, 0]
    if tipos:
        for tipo in tipos:
            total_tipos[tipo[0] - 1] += tipo[1]

    return render_template("reportes/cantTipo.html", total_tipos=total_tipos)


def cantMes():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    anio = request.args.get("anio", "2021")

    estudios = (
        db.session.query(Estudio.fecha, func.count(Estudio.mes))
        .filter(
            and_(
                Estudio.fecha >= str(anio) + "-01-01",
                Estudio.fecha <= str(anio) + "-12-31",
            )
        )
        .group_by(Estudio.mes)
        .all()
    )

    meses_totales = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if estudios:
        for fecha, cant in estudios:
            meses_totales[fecha.month - 1] += cant

    return render_template(
        "reportes/cantMes.html", meses_totales=meses_totales, anio=anio
    )


def boxPlot():

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    lista = []

    anio = request.args.get("boxplot", "2021")

    estudios = (
        Estudio.query.filter(
            and_(
                Estudio.fecha >= str(anio) + "-01-01",
                Estudio.fecha <= str(anio) + "-12-31",
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
        "reportes/boxplot.html", min=min, max=max, q1=q1, q2=q2, q3=q3, anio=anio
    )
