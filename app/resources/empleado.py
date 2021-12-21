from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.user import User
from app.models.rol import Rol
from app.helpers.auth import authenticated
from app.db import db
from datetime import datetime
from operator import or_

# Protected resources
def index():
    """lista los usuarios del sistema"""

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 1):  # rol admin
        abort(401)

    users = User.query.filter(User.rol == 2).all()
    return render_template("admin/empleado_index.html", users=users)


def new():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 1):
        abort(401)

    return render_template("admin/empleado_new.html")


def create():
    """función para alta de usuario"""

    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 1):
        abort(401)

    # con los asteriscos convierto los parametros del diccionario, a parametros separados que requiere mi constructor
    params = request.form

    user = User.query.filter(
        or_(User.email == params["email"], User.dni == params["dni"])
    ).first()
    if user:
        flash("El Email o DNI ingresados ya existe", "error")
        return redirect(url_for("empleado_new"))

    new_user = User(
        first_name=params["first_name"],
        last_name=params["last_name"],
        dni=params["dni"],
        email=params["email"],
        password=params["password"],
        rol=2,
    )

    flash("Alta exitosa de empleado", "success")

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("empleado_index"))


def edit():
    """permite acceder al formulario para editar usuario"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 1):
        abort(401)

    roles = Rol.query.all()
    user_id = request.args.get("id")
    user = db.session.query(User).filter(User.id == user_id).one()

    return render_template("admin/empleado_edit.html", user=user, roles=roles)


def update():
    """formulario para editar usuario"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 1):
        abort(401)

    params = request.form
    user_id_editar = request.args.get("id")
    user = User.query.filter_by(id=user_id_editar).first()
    user.first_name = params["first_name"]
    user.last_name = params["last_name"]
    user.password = params["password"]
    user.updated_at = datetime.now()

    db.session.commit()

    flash("Los datos del empleado han sido modificados exitosamente", "success")
    return redirect(url_for("empleado_index"))


def swichtstate():
    """funcion para cambiar el estado de un usuario de activo a bloqueado y viceversa"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 1):
        abort(401)

    if request.args.get("activo") == "True":
        user_estado = False
        intentos = 3
    else:
        user_estado = True
        intentos = 0

    user_id = request.args.get("id")

    u = User.query.filter_by(id=user_id).first()
    u.activo = user_estado
    u.intentos = intentos
    db.session.commit()

    flash("El estado del empleado ha sido modificado exitosamente", "success")

    return redirect(url_for("empleado_index"))
