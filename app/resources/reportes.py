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


def cant_estudios_tipo():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    tipos = (
        db.session.query(Estudio.tipoEstudio, func.count(Estudio.tipoEstudio))
        .group_by(Estudio.tipoEstudio)
        .all()
    )
    total_tipos = []
    flash(tipos)
    for i in range(1, 6):
        total = 0
        flash(i)
        for t in tipos:
            flash(t)
            if i == t[0]:
                flash(i)
                flash(t[0])
                total += t[1]
        total_tipos.append(total)
    flash(total_tipos)

    # flash(t[0]) #tipo
    # todos_estudios
    # flash(t[1])#cantidad
    # return render_template("empleados/index.html", tipos=tipos)
    return render_template("reportes/cant_estudios_tipo.html", total_tipos=total_tipos)


def cant_estudios_mes_anio():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    # anio_buscado= request.form
    meses = (
        db.session.query(Estudio.fecha, func.count(Estudio.fecha))
        .group_by(
            func.date(Estudio.fecha) >= "2021-01-01",
            func.date(Estudio.fecha) <= "2021-12-31",
        )
        .group_by(Estudio.mes)
    )
    meses_totales = []
    for i in range(1, 13):
        total = 0
        flash(i)
        for m in meses:
            mes = m[0]
            flash(mes)
            if i == m[0]:
                flash(i)
                flash(m[0])
                total += m[1]
        meses_totales.append(total)

    flash(meses_totales)
    return render_template(
        "reportes/cant_estudios_mes_anio.html", meses_totales=meses_totales
    )
