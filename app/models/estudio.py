from app.models.estado import Estado
from app.models.rol import Rol
from app.models.permiso import Permiso
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
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
    presupuesto = Column(Integer)
    resultado_id = Column(Integer, ForeignKey("resultados.id"), nullable=True)
    resultado = relationship("Resultado")
    extraccion_id = Column(Integer, ForeignKey("extracciones.id"), nullable=True)
    extraccion = relationship("Extraccion")
    estadoActual = Column(Integer, nullable=True)
    estados = relationship("Estado")


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
