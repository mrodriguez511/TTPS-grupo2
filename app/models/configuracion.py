from app.db import db
from sqlalchemy import Column, Integer, String, Boolean


class Configuracion(db.Model):
    __tablename__ = "configuracion"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pacienteObligado = Column(Boolean)

    def __init__(self, pacienteObligado=None):
        self.pacienteObligado = pacienteObligado

    def check_config():
        config = Configuracion.query.first()
        return config
