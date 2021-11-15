from flask import redirect, render_template, session, abort
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.operators import and_
from app.models.lote import Lote

from app.models.estudio import Estudio

from app.helpers.auth import authenticated
from app.db import db

# muestra todos los lotes que no tienen URL de resultado
def index():

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    lotes = Lote.query.filter(Lote.url == null).all

    return render_template("lotesEsperandoURL/index.html", lotes=lotes)
