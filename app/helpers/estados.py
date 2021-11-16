from flask import session
from app.models.estado import Estado
from app.db import db


def cargarNuevoEstado(estudio):
    estudio.estados.append(Estado(estudio.estadoActual, session["id"], estudio.id))
    db.session.commit()
