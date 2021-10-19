from app.db import db
from sqlalchemy import Column, Integer, String, Boolean


class Punto_encuentro(db.Model):
    __tablename__ = "puntos_encuentro"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), primary_key=True)
    direccion = Column(String(30), primary_key=True)
    coordenadas = Column(String(100), unique=False)
    estado = Column(Boolean)
    telefono = Column(String(30), unique=True)
    email = Column(String(30), unique=False)

    def __init__(
        self, nombre=None, direccion=None, coordenadas=None, telefono=None, email=None
    ):
        self.nombre = nombre
        self.direccion = direccion
        self.coordenadas = coordenadas
        self.estado = True
        self.telefono = telefono
        self.email = email
