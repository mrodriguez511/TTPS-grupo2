import datetime
from app.models.estado import Estado
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db import db
from sqlalchemy.orm import relationship


class Estudio(db.Model):
    __tablename__ = "estudios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(datetime, unique=False)
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
    estadoActual = Column(Integer)
    estados = relationship("Estado")
    factura = Column(String(100), nullable=True)
    comprobanteFactura = Column(String(100), nullable=True)
    consentimientoFirmado = Column(String(100), nullable=True)
    empleadoMuestra = Column(String(100), nullable=True)
    urlResultado = Column(String(100), nullable=True)
    turno = Column(datetime, nullable=True)
    muestra_ml = Column(Integer, nullable=True)
    muestra_freezer = Column(Integer, nullable=True)
    resultadoEnviado = Column(Boolean, nullable=True)
    extraccionAbonada = Column(Boolean, nullable=True)
    lote = Column(Integer, ForeignKey("lotes.id"), nullable=True)


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
    self.fecha = datetime.now()
    self.retrasado = False
    self.anulado = False
    self.estadoActual = 1

    estado1 = Estado(1, empleado, self)
    self.estados = [estado1]
