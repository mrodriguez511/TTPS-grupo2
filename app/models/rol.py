from sqlalchemy import Column, Integer, String
from app.db import db
from sqlalchemy.orm import relationship
from app.models.roles_permisos import roles_permisos
from app.models.users_roles import users_roles


class Rol(db.Model):

    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)
    users = relationship("User", secondary=users_roles, back_populates="roles")
    permisos = relationship("Permiso", secondary=roles_permisos, back_populates="roles")

    def __init__(self, name=None):
        self.name = name
