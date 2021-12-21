from datetime import datetime

from sqlalchemy.sql.sqltypes import Date
from app.models.estado import Estado
from app.models.resultado import Resultado
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from app.db import db
from sqlalchemy.orm import relationship
from flask import session
from app.helpers.auth import authenticated


class Estudio(db.Model):
    __tablename__ = "estudios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime)
    mes = Column(Integer)
    retrasado = Column(Boolean)
    anulado = Column(Boolean)
    comprobanteValido = Column(Boolean)
    tipoEstudio = Column(Integer, ForeignKey("tiposEstudios.id"))
    medicoDerivante = Column(Integer, ForeignKey("medicosDerivantes.id"))
    medicoInformante = Column(Integer, ForeignKey("medicosInformantes.id"))
    paciente = Column(Integer, ForeignKey("pacientes.id"))
    empleado = Column(Integer, ForeignKey("users.id"))
    diagnosticoPresuntivo = Column(Integer, ForeignKey("diagnosticosPresuntivos.id"))
    presupuesto = Column(Integer)
    resultado = relationship(Resultado)
    resultado_id = Column(Integer, ForeignKey("resultados.id"))
    estadoActual = Column(Integer)
    estados = relationship("Estado")
    archivoPresupuesto = Column(String(100), nullable=True)
    comprobanteDePago = Column(String(100), nullable=True)
    consentimientoFirmado = Column(String(100), nullable=True)
    empleadoMuestra = Column(String(100), nullable=True)
    turno = Column(DateTime, nullable=True)
    muestra_ml = Column(Float, nullable=True)
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
        self.mes = datetime.now().month
        self.retrasado = False
        self.anulado = False
        self.extraccionAbonada = False
        self.resultadoEnviado = False
        self.comprobanteValido = False
        self.estadoActual = 1
        if authenticated(session):
            id = session["id"]
        else:
            id = 1
        self.estados = [Estado(1, id, self.id)]
