from sqlalchemy.sql.functions import now
from app.db import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.punto_encuentro import TipoEstudio, diagnosticoPresuntivo, obraSocial


class EsperandoComprobantePago(db.Model):
    __tablename__ = "EsperandoComprobantePago"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime)
    empleado = Column(Integer, ForeignKey("empleados.id"))
    obraSocial = Column(String(30))
    diagnosticoPresuntivo = Column(String(30))
    tipoEstudio = Column(String(30))
    presupuesto = Column(String(30))

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
