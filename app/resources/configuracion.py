from flask import redirect, render_template, request, url_for, session, abort
from app.models.configuracion import Configuracion
from app.helpers.auth import authenticated
from app.db import db


def index():
    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 4):
        abort(401)

    config = Configuracion.query.first()

    return render_template("configurador/home.html", config=config)


def configurar():
    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 4):
        abort(401)

    params = request.form["config"]
    config = Configuracion.query.first()

    config.pacienteObligado = int(params)

    db.session.commit()

    return redirect(url_for("configurador_home"))
