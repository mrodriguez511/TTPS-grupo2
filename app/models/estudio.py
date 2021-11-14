from datetime import datetime
from app.models.estado import Estado
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.db import db
from sqlalchemy.orm import relationship
from flask import session


class Estudio(db.Model):
    __tablename__ = "estudios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime)
    retrasado = Column(Boolean)
    anulado = Column(Boolean)
    tipoEstudio = Column(Integer, ForeignKey("tiposEstudios.id"))
    medicoDerivante = Column(Integer, ForeignKey("medicosDerivantes.id"))
    paciente = Column(Integer, ForeignKey("pacientes.id"))
    empleado = Column(Integer, ForeignKey("users.id"))
    diagnosticoPresuntivo = Column(Integer, ForeignKey("diagnosticosPresuntivos.id"))
    presupuesto = Column(Integer)
    resultado_id = Column(Integer, ForeignKey("resultados.id"))
    resultado = relationship("Resultado",foreign_keys=[resultado_id]),allowNull: false
    estadoActual = Column(Integer)
    estados = relationship("Estado")
    archivoPresupuesto = Column(String(100), nullable=True)
    comprobanteDePago = Column(String(100), nullable=True)
    consentimientoFirmado = Column(String(100), nullable=True)
    empleadoMuestra = Column(String(100), nullable=True)
    turno = Column(DateTime, nullable=True)
    muestra_ml = Column(Integer, nullable=True)
    muestra_freezer = Column(Integer, nullable=True)
    resultadoEnviado = Column(Boolean, nullable=True)
    extraccionAbonada = Column(Boolean, nullable=True)
    #lote = Column(Integer, ForeignKey("lotes.id"), nullable=True)

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
        self.estados = [Estado(1, session["id"], self.id)]
