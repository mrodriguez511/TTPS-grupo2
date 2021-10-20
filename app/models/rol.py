from sqlalchemy import Column, Integer, String
from app.db import db
from sqlalchemy.orm import relationship
from app.models.roles_permisos import roles_permisos




class Rol(db.Model):

    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)
    relationship("User")
    permisos = relationship("Permiso", secondary=roles_permisos, back_populates="roles")


    def __init__(self, name=None):
        self.name = name
