from sqlalchemy import Column, Integer, String, Boolean
from app.db import db
from sqlalchemy.orm import relationship


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
