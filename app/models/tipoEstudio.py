from sqlalchemy import Column, Integer, String, Boolean
from app.db import db
from sqlalchemy.orm import relationship


class TipoEstudio(db.Model):

    __tablename__ = "tiposEstudios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True)
    consentimientoInformado = Column(String(300))
    # estudios = relationship("Estudio", backref="tipoEstudio")
    estudios = relationship("Estudio")

    def __init__(
        self,
        nombre=None,
        consentimientoInformado=None,
    ):
        self.nombre = nombre
        self.consentimientoInformado = consentimientoInformado
