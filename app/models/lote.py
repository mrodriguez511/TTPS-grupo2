from app.models.rol import Rol
from sqlalchemy import Column, Integer, String, Boolean, Date, and_, ForeignKey
from datetime import datetime
from app.db import db
from sqlalchemy.orm import relationship


class Lote(db.Model):
    __tablename__ = "lotes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(300), nullable=True)
    estudios = relationship("Estudio")


def __init__(self, estudios=None):
    self.estudios = [estudios]
