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
from app.models.tipoEstudio import TipoEstudio
from datetime import date
from datetime import datetime
from sqlalchemy import func
from flask import flash


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
