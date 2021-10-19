from sqlalchemy import Column, Integer
from app.db import db
from sqlalchemy.sql.schema import ForeignKey


users_roles = db.Table(
    "users_roles",
    db.Model.metadata,
    Column("users", Integer, ForeignKey("users.id"), primary_key=True),
    Column("roles", Integer, ForeignKey("roles.id"), primary_key=True),
)
