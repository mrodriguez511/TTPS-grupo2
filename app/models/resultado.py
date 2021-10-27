from sqlalchemy import Column, Integer, String, Boolean
from app.db import db
from sqlalchemy.orm import relationship


class Resultado(db.Model):

    __tablename__ = "resultados"
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Boolean)
    detalle = Column(String(200), unique=False)
    # permisos = relationship("Permiso", secondary=roles_permisos, back_populates="roles")

    def __init__(self, valor=None, detalle=None):
        self.valor = valor
        self.detalle = detalle
