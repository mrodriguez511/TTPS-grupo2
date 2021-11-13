from sqlalchemy import Column, Integer, String
from app.db import db
from sqlalchemy.orm import relationship


class Rol(db.Model):

    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)
    usuarios = relationship("User")

    def __init__(self, name=None):
        self.name = name
