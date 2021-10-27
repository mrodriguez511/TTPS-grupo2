from sqlalchemy import Column, Integer, String, Boolean
from app.db import db
from sqlalchemy.orm import relationship


class TipoEstudio(db.Model):

    __tablename__ = "tiposEstudios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True)
    consentimientoInformado = Column(String(300))
    precioEstudio = Column(Integer)
    precioExtraccion = Column(Integer)

    def __init__(
        self,
        nombre=None,
        consentimientoInformado=None,
        precioEstudio=None,
        precioExtraccion=None,
    ):
        self.nombre = nombre
        self.consentimientoInformado = consentimientoInformado
        self.precioEstudio = precioEstudio
        self.precioExtraccion = precioExtraccion
