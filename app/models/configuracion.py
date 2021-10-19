from app.db import db
from sqlalchemy import Column, Integer, String, Boolean


class Configuracion(db.Model):
    __tablename__ = "configuracion"
    id = Column(Integer, primary_key=True, autoincrement=True)
    paginado = Column(Integer, unique=False)
    paleta_AppPublica = Column(String(30), unique=False)
    paleta_AppPrivada = Column(String(30), unique=False)
    ordenacion = Column(Boolean)

    def __init__(
        self,
        paginado=None,
        paleta_AppPublica=None,
        paleta_AppPrivada=None,
        ordenacion=None,
    ):
        self.paginado = paginado
        self.paleta_AppPublica = paleta_AppPublica
        self.paleta_AppPrivada = paleta_AppPrivada
        self.ordenacion = ordenacion

    def check_config():
        config = Configuracion.query.first()
        return config
