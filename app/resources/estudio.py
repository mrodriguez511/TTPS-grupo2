from flask import redirect, render_template, request, url_for, session, abort, flash
from app.helpers.archivos import generar_factura
from app.models.user import User
from app.models.rol import Rol

from app.models.punto_encuentro import (
    Paciente,
    MedicoDerivante,
    DiagnosticoPresuntivo,
    TipoEstudio,
)
from app.helpers.auth import authenticated
from app.db import db
from datetime import datetime

# import pdfkit

# Protected resources
def index():
    """listado de estudios"""

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    return render_template("empleados/index.html")


def new_estudio():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    pacientes = Paciente.query.all()
    medicos = MedicoDerivante.query.all()
    diagnoticos = DiagnosticoPresuntivo.query.all()
    tipos = TipoEstudio.query.all()

    return render_template(
        "estudio/alta.html",
        pacientes=pacientes,
        medicos=medicos,
        diagnosticos=diagnoticos,
        tipos=tipos,
    )


def create_estudio():
    """función para alta de estudio"""

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

    return redirect(url_for("estudio_estado1"))


def estudio_estado1():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    """if not check_permission(session["id"], "user_new"):
        abort(401)"""
    estudio = "555"

    # factura = os.path.join(current_app.root_path, app.config["UPLOAD_FOLDER"])
    factura = "archivos/facturas/factura_" + "555" + ".pdf"
    return render_template("estudio/estado1.html", estudio=estudio, factura=factura)


def estudio_estado1_carga():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    """if not check_permission(session["id"], "user_new"):
        abort(401)"""

    return render_template("estudio/estado_1.html")
