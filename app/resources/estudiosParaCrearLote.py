from flask import redirect, render_template, session, abort
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.operators import and_

from app.models.estudio import Estudio
from app.models.paciente import Paciente
from app.models.tipoEstudio import TipoEstudio


from app.helpers.auth import authenticated
from app.db import db

# muestra todos los estudios cuyo estado actual es 6 (Esperando formar lote)
def index():

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    estudios = (
        db.session.query(Estudio, Paciente, TipoEstudio)
        .filter(Estudio.paciente == Paciente.id)
        .filter(Estudio.tipoEstudio == TipoEstudio.id)
        .filter(Estudio.estadoActual == 6)
        .all()
    )

    return render_template("estudiosParaCrearLote/index.html", estudios=estudios)
