from app.models.rol import Rol
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
)
from datetime import datetime
from app.db import db
from sqlalchemy.orm import relationship


class Paciente(db.Model):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=False)
    apellido = Column(String(30), unique=False)
    fechaNacimiento = Column(Date, unique=False)
    email = Column(String(30), unique=True)
    dni = Column(Integer, unique=True)
    telefono = Column(String(30), unique=True)
    resumenHC = Column(String(300), unique=True)
    password = Column(String(30), unique=False)
    nroAfiliado = Column(Integer, unique=True, nullable=True)
    obraSocial = Column(Integer, ForeignKey("obrasSociales.id"), nullable=True)
    estudios = relationship("Estudio", backref="paciente")

    def __init__(
        self,
        nombre=None,
        apellido=None,
        dni=None,
        fechaNacimiento=None,
        email=None,
        telefono=None,
        resumenHC=None,
        nroAfiliado=None,
        obraSocial=None,
    ):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.fechaNacimiento = fechaNacimiento
        self.email = email
        self.telefono = telefono
        self.resumenHC = resumenHC
        self.password = dni
        self.nroAfiliado = nroAfiliado
        self.obraSocial = obraSocial
