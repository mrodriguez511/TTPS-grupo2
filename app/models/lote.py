from app.models.rol import Rol

# from app.models.permiso import Permiso
from sqlalchemy import Column, Integer, String, Boolean, Date, and_, ForeignKey
from datetime import datetime
from app.db import db
from sqlalchemy.orm import relationship


class Lote(db.Model):
    __tablename__ = "lotes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(300), nullable=True)  # cambiado (300)
    estudios = relationship("Estudio")


def __init__(self, estudios=None):
    self.estudios = [estudios]
