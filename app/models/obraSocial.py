from sqlalchemy import Column, Integer, String
from app.db import db
from sqlalchemy.orm import relationship


class obraSocial(db.Model):

    __tablename__ = "obrasSociales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=True)
    pacientes = relationship("Paciente")
    # permisos = relationship("Permiso", secondary=roles_permisos, back_populates="roles")

    def __init__(self, nombre=None):
        self.nombre = nombre
