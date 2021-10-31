from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.user import User
from app.models.rol import Rol
from app.helpers.auth import authenticated
from app.db import db
from datetime import datetime

# Protected resources
def index():
    """lista los usuarios del sistema"""

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 1):  # rol admin
        abort(401)

    users = User.query.filter(User.borrado != True, User.id != session["id"]).all()
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

    user = User.query.filter(User.email == params["email"]).first()
    if user:
        flash("El Email ingresado ya existe")
        return redirect(url_for("empleado_new"))

    new_user = User(
        first_name=params["first_name"],
        last_name=params["last_name"],
        dni=params["dni"],
        email=params["email"],
        password=params["password"],
        rol=2,
    )

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

    return redirect(url_for("empleado_index"))


def delete():
    """función para eliminar usuario"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 1):
        abort(401)
    if request.args.get("id") == session["id"]:
        flash("Operación NO permitida")
    user_id_eliminar = request.args.get("id")
    user_eliminar = db.session.query(User).filter(User.id == user_id_eliminar).one()
    user_eliminar.borrado = True
    db.session.commit()

    return redirect(url_for("empleado_index"))


def swichtstate():
    """funcion para cambiar el estado de un usuario de activo a bloqueado y viceversa"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 1):
        abort(401)

    if request.args.get("activo") == "True":
        user_estado = False
    else:
        user_estado = True

    if request.args.get("id") == session["id"]:
        flash("Operación NO permitida")

    # user_estado = not request.args.get("activo")
    user_id = request.args.get("id")

    User.query.filter_by(id=user_id).update(
        dict(activo=user_estado, updated_at=datetime.now())
    )
    db.session.commit()  # Guardamos los cambios con commit

    return redirect(url_for("empleado_index"))
