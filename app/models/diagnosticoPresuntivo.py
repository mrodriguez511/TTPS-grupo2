from sqlalchemy import Column, Integer, String
from app.db import db
from sqlalchemy.orm import relationship


class diagnosticoPresuntivo(db.Model):

    __tablename__ = "diagnosticosPresuntivos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True)
    estudios=relationship("Estudio")
    # permisos = relationship("Permiso", secondary=roles_permisos, back_populates="roles")

    def __init__(self, nombre=None):
        self.nombre = nombre
