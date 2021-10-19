from app.models.rol import Rol
from app.models.permiso import Permiso
from sqlalchemy import Column, Integer, String, Boolean, DateTime, and_
from datetime import datetime
from app.db import db
from sqlalchemy.orm import relationship
from app.models.users_roles import *


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30), unique=False)
    last_name = Column(String(30), unique=False)
    username = Column(String(30), unique=True)
    activo = Column(Boolean)
    email = Column(String(30), unique=True)
    password = Column(String(30), unique=False)
    updated_at = Column(DateTime)
    created_at = Column(DateTime)
    roles = relationship("Rol", secondary=users_roles, back_populates="users")

    def __init__(
        self, first_name=None, last_name=None, email=None, password=None, username=None
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.username = username
        self.activo = True
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @classmethod
    def has_permission(cls, user_id, permission):
        # CONSULTA si el permiso consultado pertenece al usuario
        permiso = (
            db.session.query(User, Rol, Permiso)
            .join(User.roles)
            .join(Rol.permisos)
            .filter(and_(User.id == user_id, Permiso.name == permission))
            .first()
        )
        if not permiso:
            return False
        return True
