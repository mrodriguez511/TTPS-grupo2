from sqlalchemy import Column, Integer, String
from app.db import db
from sqlalchemy.orm import relationship
from app.models.roles_permisos import roles_permisos


class Permiso(db.Model):

    __tablename__ = "permisos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)
    roles = relationship("Rol", secondary=roles_permisos, back_populates="permisos")

    def __init__(self, name=None):
        self.name = name
