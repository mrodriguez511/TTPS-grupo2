import datetime

from sqlalchemy.sql.sqltypes import DateTime
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


class DiagnosticoPresuntivo(db.Model):

    __tablename__ = "diagnosticosPresuntivos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True)
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


class Estado(db.Model):
    __tablename__ = "estados"
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer)
    fecha = Column(Date, unique=False)
    empleado = Column(Integer, ForeignKey("users.id"))
    estudio = Column(Integer, ForeignKey("estudios.id"))

    def __init__(self, numero=None, empleado=None, estudio=None):
        self.numero = numero
        self.empleado = empleado
        self.estudio = estudio
        self.fecha = Date.today()


class Estudio(db.Model):
    __tablename__ = "estudios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, unique=False)
    retrasado = Column(Boolean)
    anulado = Column(Boolean)
    tipoEstudio = Column(Integer, ForeignKey("tiposEstudios.id"))
    medicoDerivante = Column(Integer, ForeignKey("medicosDerivantes.id"))
    paciente = Column(Integer, ForeignKey("pacientes.id"))
    empleado = Column(Integer, ForeignKey("users.id"))
    diagnosticoPresuntivo = Column(Integer, ForeignKey("diagnosticosPresuntivos.id"))
    presupuesto = Column(Integer)
    resultado_id = Column(Integer, ForeignKey("resultados.id"), nullable=True)
    resultado = relationship("Resultado")
    estadoActual = Column(Integer, nullable=True)
    estados = relationship("Estado")
    factura = Column(String(100), nullable=True)
    comprobanteFactura = Column(String(100), nullable=True)
    consentimientoFirmado = Column(String(100), nullable=True)
    empleadoMuestra = Column(String(100), nullable=True)
    urlResultado = Column(String(100), nullable=True)
    turno = Column(DateTime, nullable=True)
    muestra_ml = Column(Integer, nullable=True)
    muestra_freezer = Column(Integer, nullable=True)
    resultadoEnviado = Column(Boolean, nullable=True)
    extraccionAbonada = Column(Boolean, nullable=True)
    lote = Column(Integer, ForeignKey("lotes.id"))

    def __init__(
        self,
        tipoEstudio=None,
        medicoDerivante=None,
        paciente=None,
        empleado=None,
        diagnosticoPresuntivo=None,
        presupuesto=None,
    ):
        self.tipoEstudio = tipoEstudio
        self.medicoDerivante = medicoDerivante
        self.paciente = paciente
        self.empleado = empleado
        self.diagnosticoPresuntivo = diagnosticoPresuntivo
        self.presupuesto = presupuesto
        self.fecha = Date.today()
        self.retrasado = False
        self.anulado = False
        self.estadoActual = 1

        estado1 = Estado(1, empleado, self)
        self.estados = [estado1]


class Lote(db.Model):
    __tablename__ = "lotes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(100), nullable=True)
    estudios = relationship("Estudio")

    def __init__(self, estudios=None):
        self.estudios = [estudios]
