from app.db import db
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.helpers.auth import authenticated
from app.models.punto_encuentro import Punto_encuentro


"""def index():

    if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "punto_encuentro_index"):
        abort(401)

    puntos_encuentro = db.session.query(Punto_encuentro).all()
    return render_template(
        "punto_encuentro/index.html", puntos_encuentro=puntos_encuentro
    )


def new():
    if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "punto_encuentro_new"):
        abort(401)

    return render_template("punto_encuentro/new.html")


def create():
    if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "punto_encuentro_create"):
        abort(401)

    params = request.form

    user = Punto_encuentro.query.filter(
        Punto_encuentro.nombre == params["nombre"]
        and Punto_encuentro.direccion == params["direccion"]
    ).first()
    if user:
        flash("Nombre y dirección de punto de encuentro ya existente")
        return redirect(url_for("punto_encuentro_new"))
    new_punto_encuentro = Punto_encuentro(
        nombre=params["nombre"],
        direccion=params["direccion"],
        coordenadas=params["coordenadas"],
        telefono=params["telefono"],
        email=params["email"],
    )

    db.session.add(new_punto_encuentro)
    db.session.commit()

    return redirect(url_for("punto_encuentro_index"))


def edit():
    if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "punto_encuentro_edit"):
        abort(401)

    punto_encuentro_id = request.args.get("id")
    punto_encuentro = (
        db.session.query(Punto_encuentro)
        .filter(Punto_encuentro.id == punto_encuentro_id)
        .one()
    )

    return render_template("punto_encuentro/edit.html", punto_encuentro=punto_encuentro)


def update():
    if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "punto_encuentro_update"):
        abort(401)

    params = request.form

    punto_encuentro_id = request.args.get("id")
    punto_encuentro = (
        db.session.query(Punto_encuentro)
        .filter(Punto_encuentro.id == punto_encuentro_id)
        .one()
    )

    punto_encuentro.coordenadas = params["coordenadas"]
    punto_encuentro.telefono = params["telefono"]
    punto_encuentro.email = params["email"]

    db.session.commit()

    return redirect(url_for("punto_encuentro_index"))


def show():
    if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "punto_encuentro_show"):
        abort(401)

    punto_encuentro_id = request.args.get("id")
    punto_encuentro = (
        db.session.query(Punto_encuentro)
        .filter(Punto_encuentro.id == punto_encuentro_id)
        .one()
    )

    return render_template("punto_encuentro/show.html", punto_encuentro=punto_encuentro)


def destroy():

    if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "punto_encuentro_destroy"):
        abort(401)
    punto_encuentro_id = request.args.get("id")
    punto_encuentro_eliminar = (
        db.session.query(Punto_encuentro)
        .filter(Punto_encuentro.id == punto_encuentro_id)
        .one()
    )
    db.session.delete(punto_encuentro_eliminar)
    db.session.commit()

    return redirect(url_for("punto_encuentro_index"))


def swichtstate():
    funcion para cambiar el estado de un punto de encuentro de publicado a despublicado y viceversa
    if not authenticated(session):
        abort(401)

    if request.args.get("activo") == "True":
        punto_encuentro_estado = False
    else:
        punto_encuentro_estado = True

    punto_encuentro_id = request.args.get("id")

    Punto_encuentro.query.filter_by(id=punto_encuentro_id).update(
        dict(estado=punto_encuentro_estado)
    )
    db.session.commit()

    return redirect(url_for("punto_encuentro_index"))
"""
