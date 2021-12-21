from flask import session
from app.models.estado import Estado
from app.db import db


def cargarNuevoEstado(estudio):
    if session["rol"] == 2:
        estudio.estados.append(Estado(estudio.estadoActual, session["id"], estudio.id))
    else:
        empleado = estudio.empleado
        estudio.estados.append(Estado(estudio.estadoActual, empleado, estudio.id))
    db.session.commit()
