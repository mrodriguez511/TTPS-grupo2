from sqlalchemy.sql.functions import now
from app.db import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.punto_encuentro import TipoEstudio, diagnosticoPresuntivo, obraSocial


class EsperandoConsentimientoFirmado(db.Model):
    __tablename__ = "EsperandoConsentimientoFirmado"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime)
    empleado = Column(Integer, ForeignKey("empleados.id"))
    obraSocial = Column(String(30))
    consentimiento = Column(String(300))

    def __init__(
        self,
        empleado=None,
        obraSocial=None,
        diagnosticoPresuntivo=None,
        tipoEstudio=None,
        presupuesto=None,
    ):
        self.empleado = empleado
        self.obraSocial = obraSocial
        self.diagnosticoPresuntivo = diagnosticoPresuntivo
        self.fecha = DateTime.now()
        self.tipoEstudio = tipoEstudio
        self.presupuesto = presupuesto
