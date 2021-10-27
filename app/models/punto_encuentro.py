from app.db import db
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship


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


class TipoEstudio(db.Model):

    __tablename__ = "tiposEstudios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True)
    consentimientoInformado = Column(String(300))
    precioEstudio = Column(Integer)
    precioExtraccion = Column(Integer)

    def __init__(
        self,
        nombre=None,
        consentimientoInformado=None,
        precioEstudio=None,
        precioExtraccion=None,
    ):
        self.nombre = nombre
        self.consentimientoInformado = consentimientoInformado
        self.precioEstudio = precioEstudio
        self.precioExtraccion = precioExtraccion


class diagnosticoPresuntivo(db.Model):

    __tablename__ = "diagnosticosPresuntivos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=True)
    # permisos = relationship("Permiso", secondary=roles_permisos, back_populates="roles")

    def __init__(self, nombre=None):
        self.nombre = nombre


class Extraccion(db.Model):

    __tablename__ = "extracciones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    realizada = Column(Boolean)
    abonada = Column(Boolean)
    precio = Column(Integer)
    # permisos = relationship("Permiso", secondary=roles_permisos, back_populates="roles")

    def __init__(self):
        self.realizada = False
        self.abonada = False


class MedicoDerivante(db.Model):

    __tablename__ = "medicosDerivantes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=False)
    apellido = Column(String(30), unique=False)
    matricula = Column(String(30), unique=True)
    mail = Column(String(30), unique=True)
    # permisos = relationship("Permiso", secondary=roles_permisos, back_populates="roles")

    def __init__(self, nombre=None, apellido=None, matricula=None, mail=None):
        self.nombre = nombre
        self.apellido = apellido
        self.matricula = matricula
        self.mail = mail


class ObraSocial(db.Model):

    __tablename__ = "obrasSociales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=True)
    pacientes = relationship("Paciente")
    # permisos = relationship("Permiso", secondary=roles_permisos, back_populates="roles")

    def __init__(self, nombre=None):
        self.nombre = nombre


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
    nroAfiliado = Column(String(30), unique=True, nullable=True)
    obraSocial = Column(Integer, ForeignKey("obrasSociales.id"), nullable=True)

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


class Resultado(db.Model):

    __tablename__ = "resultados"
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Boolean)
    detalle = Column(String(200), unique=False)
    # permisos = relationship("Permiso", secondary=roles_permisos, back_populates="roles")

    def __init__(self, valor=None, detalle=None):
        self.valor = valor
        self.detalle = detalle
