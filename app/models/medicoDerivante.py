"""from sqlalchemy import Column, Integer, String
from app.db import db
from sqlalchemy.orm import relationship


class MedicoDerivante(db.Model):

    __tablename__ = "medicosDerivantes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=False)
    apellido = Column(String(30), unique=False)
    matricula = Column(String(30), unique=True)
    mail = Column(String(30), unique=True)
    estudios = relationship("Estudio")
    # permisos = relationship("Permiso", secondary=roles_permisos, back_populates="roles")

    def __init__(self, nombre=None, apellido=None, matricula=None, mail=None):
        self.nombre = nombre
        self.apellido = apellido
        self.matricula = matricula
        self.mail = mail"""
