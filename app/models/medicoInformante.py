from sqlalchemy import Column, Integer, String
from app.db import db
from sqlalchemy.orm import relationship


class MedicoInformante(db.Model):

    __tablename__ = "medicosInformantes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=False)
    apellido = Column(String(30), unique=False)
    matricula = Column(String(30), unique=True)
    estudios = relationship("Estudio")

    def __init__(self, nombre=None, apellido=None, matricula=None):
        self.nombre = nombre
        self.apellido = apellido
        self.matricula = matricula
