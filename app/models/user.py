from app.models.rol import Rol
from sqlalchemy import Column, Integer, String, Boolean, DateTime, and_, ForeignKey
from datetime import datetime
from app.db import db
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30), unique=False)
    last_name = Column(String(30), unique=False)
    dni = Column(Integer, primary_key=True, unique=True)
    email = Column(String(30), unique=True)
    password = Column(String(30), unique=False)
    borrado = Column(Boolean)
    rol = Column(Integer, ForeignKey("roles.id"))

    def __init__(
        self,
        first_name=None,
        last_name=None,
        dni=None,
        email=None,
        password=None,
        rol=None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.dni = dni
        self.email = email
        self.password = password
        self.borrado = False
        self.rol = rol
