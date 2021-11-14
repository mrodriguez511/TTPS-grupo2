from sqlalchemy import Column, Integer, String, Boolean
from app.db import db
from sqlalchemy.orm import relationship


class Resultado(db.Model):

    __tablename__ = "resultados",db.Model.metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Boolean)
    detalle = Column(String(200), unique=False)
    #estudio = relationship("Estudio", uselist=False, backref="resultado")
   

    def __init__(self, valor=None, detalle=None):
        self.valor = valor
        self.detalle = detalle
