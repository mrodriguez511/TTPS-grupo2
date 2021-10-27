from app.models.rol import Rol
from app.models.permiso import Permiso
from sqlalchemy import Column, Integer, String, Boolean, Date, and_, ForeignKey
from datetime import datetime
from app.db import db
from sqlalchemy.orm import relationship


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
    resultado_id = Column(Integer, ForeignKey("resultados.id"))
    resultado = relationship("Resultado")
    extraccion_id = Column(Integer, ForeignKey("extracciones.id"))
    extraccion = relationship("Extraccion")
    estadoActual = nroAfiliado = Column(String(30), nullable=True)


"""
Estados

"""


def __init__(
    self,
    first_name=None,
    last_name=None,
    dni=None,
    email=None,
    password=None,
    rol=None,
):
    self.first_name = first_name
    self.last_name = last_name
    self.dni = dni
    self.email = email
    self.password = password
    self.borrado = False
    self.rol = rol
    # presupuesto= tipoEstudio.precioEstudio
