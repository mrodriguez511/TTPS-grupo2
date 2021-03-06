from app.models.rol import Rol
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from datetime import datetime
from app.db import db
from sqlalchemy.orm import relationship


class Paciente(db.Model):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=False)
    apellido = Column(String(30), unique=False)
    fechaNacimiento = Column(Date, unique=False)
    email = Column(String(30), unique=False)
    dni = Column(Integer, unique=True)
    telefono = Column(String(30))
    resumenHC = Column(String(300))
    direccion = Column(String(300))
    password = Column(String(30), unique=False)
    nombre_tutor = Column(String(30), unique=False, nullable=True)
    apellido_tutor = Column(String(30), unique=False, nullable=True)
    menor = Column(Boolean)
    nroAfiliado = Column(Integer, unique=True, nullable=True)
    obraSocial = Column(Integer, ForeignKey("obrasSociales.id"), nullable=True)
    estudios = relationship("Estudio")
    rol = Column(Integer, ForeignKey("roles.id"))

    def __init__(
        self,
        nombre=None,
        apellido=None,
        dni=None,
        fechaNacimiento=None,
    ):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.fechaNacimiento = fechaNacimiento
        self.rol = 3
