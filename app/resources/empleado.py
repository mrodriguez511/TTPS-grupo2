from flask import redirect, render_template, request, url_for, session, abort, flash
from app.helpers.archivos import generar_factura
from app.models.user import User
from app.models.rol import Rol

from app.models.punto_encuentro import Paciente, MedicoDerivante
from app.helpers.auth import authenticated
from app.db import db
from app.helpers.check import check_permission
from datetime import datetime

# import pdfkit

# Protected resources
def index():
    """listado de estudios"""

    if not authenticated(session):
        abort(401)

    """if not check_permission(session["id"], "user_index"):
        abort(401)"""

    return render_template("empleados/index.html")


def new_estudio():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    """if not check_permission(session["id"], "user_new"):
        abort(401)"""

    pacientes = Paciente.query.all()
    medicos = MedicoDerivante.query.all()

    return render_template("estudio/alta.html", pacientes=pacientes,medicos=medicos)


def new_paciente():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    """if not check_permission(session["id"], "user_new"):
        abort(401)"""

    return render_template("estudio/alta_paciente.html")


def create_paciente():
    """función para alta de paciente"""

    """if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "user_create"):
        abort(401)"""

    # con los asteriscos convierto los parametros del diccionario, a parametros separados que requiere mi constructor
    params = request.form

    """ chequear datos que no se pueden repetir
    user = User.query.filter(User.email == params["email"]).first()
    if user:
        flash("El Email ingresado ya existe")
        return redirect(url_for("user_new"))"""

    """ consulta para agregar a la base
    new_user = User(
        first_name=params["first_name"],
        last_name=params["last_name"],
        dni=params["dni"],
        email=params["email"],
        password=params["password"],
        rol=2,
    )

    db.session.add(new_user)
    db.session.commit()"""

    return redirect(url_for("estudio_new"))


def create_estudio():
    """función para alta de usuario"""

    """if not authenticated(session):
        abort(401)
    if not check_permission(session["id"], "user_create"):
        abort(401)"""

    # con los asteriscos convierto los parametros del diccionario, a parametros separados que requiere mi constructor
    params = request.form

    """user = User.query.filter(User.email == params["email"]).first()
    if user:
        flash("El Email ingresado ya existe")
        return redirect(url_for("user_new"))

    new_user = User(
        first_name=params["first_name"],
        last_name=params["last_name"],
        dni=params["dni"],
        email=params["email"],
        password=params["password"],
        rol=2,
    )

    db.session.add(new_user)
    db.session.commit()"""

    """html = render_template("pdfs/presupuesto.html", estudio="ssdfsdfsd")
    nombre_archivo = "archivos/factura_"+ params.estudio.id;
    path_wkthmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"

    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

    pdfkit.from_string(html, "archivos/SOF.pdf", configuration=config)"""

    generar_factura("asdasd")
    # pdfkit.from_string("Hello!", "archivos/out.pdf", configuration=config)

    return redirect(url_for("estudio_new"))
