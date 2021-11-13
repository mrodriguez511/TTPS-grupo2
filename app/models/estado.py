from app.db import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, and_, ForeignKey


class Estado(db.Model):
    __tablename__ = "estados"
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer)
    fecha = Column(DateTime, unique=False)
    empleado = Column(Integer, ForeignKey("users.id"))
    estudio = Column(Integer, ForeignKey("estudios.id"))

    def __init__(self, numero=None, empleado=None, estudio=None):
        self.numero = numero
        self.empleado = empleado
        self.estudio = estudio
        self.fecha = datetime.now()
