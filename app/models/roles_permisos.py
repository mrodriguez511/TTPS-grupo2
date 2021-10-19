from sqlalchemy import Column, Integer
from app.db import db
from sqlalchemy.sql.schema import ForeignKey


roles_permisos = db.Table(
    "roles_permisos",
    db.Model.metadata,
    Column("roles", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permisos", Integer, ForeignKey("permisos.id"), primary_key=True),
)
