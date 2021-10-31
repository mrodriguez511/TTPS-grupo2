from flask import redirect, render_template, request, url_for, session, abort
from app.models.configuracion import Configuracion
from app.helpers.auth import authenticated
from app.db import db


def edit():
    """permite acceder al formulario para editar usuario"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 3):
        abort(401)

    config = Configuracion.query.first()

    return render_template("settings/settings.html", config=config)


def update():
    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 3):
        abort(401)

    params = request.form
    config = Configuracion.query.first()

    config.paginado = params["paginado"]
    config.paleta_AppPublica = params["paleta_AppPublica"]
    config.paleta_AppPrivada = params["paleta_AppPrivada"]

    config.ordenacion = int(params["ordenacion"])

    db.session.commit()

    return redirect(url_for("home"))
