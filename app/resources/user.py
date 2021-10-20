from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.user import User
from app.models.rol import Rol
from app.helpers.auth import authenticated
from app.db import db
from app.helpers.check import check_permission
from datetime import datetime

# Protected resources
def index():
    """lista los usuarios del sistema"""

    if not authenticated(session):
        abort(401)

    # if not check_permission(session["id"], "user_index"):
    #    abort(401)

    if session["rol"] == 1:
        users = db.session.query(User).all()
        # filtrar los borrads y al admin
        return render_template("user/index.html", users=users)

    return render_template("empleados/index.html")


def new():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "user_new"):
        abort(401)

    return render_template("user/new.html")


def create():
    """función para alta de usuario"""

    if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "user_create"):
        abort(401)

    # con los asteriscos convierto los parametros del diccionario, a parametros separados que requiere mi constructor
    params = request.form

    user = User.query.filter(User.email == params["email"]).first()
    if user:
        flash("El Email ingresado ya existen")
        return redirect(url_for("user_new"))

    new_user = User(
        first_name=params["first_name"],
        last_name=params["last_name"],
        email=params["email"],
        password=params["password"],
        username=params["username"],
    )

    check_rol = params.getlist("checkbox_rol")

    add_roles = []
    for id_rol in check_rol:
        rol = Rol.query.filter(Rol.id == id_rol).first()
        add_roles.append(rol)

    new_user.roles = add_roles

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("user_index"))


def edit():
    """permite acceder al formulario para editar usuario"""
    if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "user_edit"):
        abort(401)

    roles = Rol.query.all()
    user_id = request.args.get("id")
    user = db.session.query(User).filter(User.id == user_id).one()

    return render_template("user/edit.html", user=user, roles=roles)


def update():
    """formulario para editar usuario"""
    if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "user_update"):
        abort(401)

    params = request.form
    user_id_editar = request.args.get("id")
    user = User.query.filter_by(id=user_id_editar).first()
    user.first_name = params["first_name"]
    user.last_name = params["last_name"]
    user.password = params["password"]
    user.updated_at = datetime.now()

    check_rol = params.getlist("checkbox_rol")

    add_roles = []
    for id_rol in check_rol:
        rol = Rol.query.filter(Rol.id == id_rol).first()
        add_roles.append(rol)

    user.roles = add_roles

    db.session.commit()

    return redirect(url_for("user_index"))


def delete():
    """función para eliminar usuario"""
    if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "user_delete"):
        abort(401)
    if request.args.get("id") == session["id"]:
        flash("Operación NO permitida")
    user_id_eliminar = request.args.get("id")
    user_eliminar = db.session.query(User).filter(User.id == user_id_eliminar).one()
    db.session.delete(user_eliminar)
    db.session.commit()

    return redirect(url_for("user_index"))


def swichtstate():
    """funcion para cambiar el estado de un usuario de activo a bloqueado y viceversa"""
    if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "user_delete"):
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

    return redirect(url_for("user_index"))
