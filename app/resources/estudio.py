from flask import redirect, render_template, request, url_for, session, abort, flash
from flask import (
    redirect,
    render_template,
    request,
    url_for,
    session,
    abort,
    flash,
    current_app,
)
import sqlalchemy
from sqlalchemy.sql.sqltypes import DateTime
from werkzeug.utils import send_from_directory
from app.helpers.archivos import generar_factura
from app.helpers.estados import cargarNuevoEstado
from app.models.estado import Estado
from app.models.estudio import Estudio
from app.models.user import User
from app.models.resultado import Resultado
from app.models.rol import Rol
import os
from datetime import date, datetime
from app.models.diagnosticoPresuntivo import DiagnosticoPresuntivo
from app.models.paciente import Paciente
from app.models.tipoEstudio import TipoEstudio
from app.models.medicoDerivante import MedicoDerivante
from app.helpers.auth import authenticated
from app.db import db
from datetime import datetime
from operator import and_
from sqlalchemy.sql.operators import ilike_op

# import pdfkit

# Protected resources
def index():
    """listado de estudios"""

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    estudios = (
        db.session.query(Estudio, Paciente, TipoEstudio)
        .filter(Estudio.paciente == Paciente.id)
        .filter(Estudio.tipoEstudio == TipoEstudio.id)
        .all()
    )

    return render_template("estudio/index.html", estudios=estudios)


def listar():
    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    return render_template("empleados/index.html")


def ver():
    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("id")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    return redirect(
        url_for("estudio_estado" + str(estudio.estadoActual), estudio=estudio.id)
    )


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

    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    params = request.form

    new_estudio = Estudio(
        tipoEstudio=params["tipoEstudio"],
        medicoDerivante=params["medicoDerivante"],
        paciente=params["paciente"],
        empleado=session["id"],
        diagnosticoPresuntivo=params["diagnostico"],
        presupuesto=params["presupuesto"],
    )
    # new_estudio.archivoPresupuesto = generar_factura(new_estudio)

    db.session.add(new_estudio)
    archivo = generar_factura(new_estudio)  # genero el estudio
    new_estudio.archivoPresupuesto = archivo
    db.session.commit()

    return redirect(url_for("estudio_estado1", estudio=new_estudio.id))


def estudio_estado1():
    """permite acceder al formulario para alta de usuario"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()
    # prueba = "factura_9.pdf"
    ruta = current_app.config["UPLOADED_FACTURAS_DEST"]
    ruta_archivo = os.path.join(ruta, estudio.archivoPresupuesto)
    # ruta_archivo = os.path.join(ruta, prueba)
    # ruta_archivo = "sdfsdf"
    return render_template(
        "estudio/estado1.html", estudio=estudio, ruta_archivo=ruta_archivo
    )


def estudio_estado1_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    archivo = request.form["comprobante"]
    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()
    estudio.comprobanteDePago = archivo
    estudio.estadoActual += 1

    # archivo = generar_factura(new_estudio) #genero el estudio
    # new_estudio.archivoPresupuesto = archivo
    # db.session.commit()

    db.session.commit()
    cargarNuevoEstado(estudio)
    # FALTA GUARDAR EL ARCHIVO Y AGREGAR EL BOTON DE DESCARGAR EL COMPROBANTE EXISTENTE
    return redirect(url_for("estudio_estado2", estudio=estudio.id))


def estudio_estado2():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    tipoEstudio = TipoEstudio.query.filter(
        TipoEstudio.id == estudio.tipoEstudio
    ).first()

    # ruta = current_app.config["UPLOADED_FACTURAS_DEST"]
    # ruta_archivo = os.path.join(ruta, estudio.archivoConsentimiento)

    # ruta_archivo = "sdfsdf"
    return render_template(
        "estudio/estado2.html",
        estudio=estudio,
        tipoEstudio=tipoEstudio,
    )


def estudio_estado2_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    archivo = request.form["consentimiento"]
    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()
    estudio.consentimientoFirmado = archivo
    estudio.estadoActual += 1

    # archivo = generar_factura(new_estudio) #genero el estudio
    # new_estudio.archivoPresupuesto = archivo
    # db.session.commit()

    db.session.commit()
    cargarNuevoEstado(estudio)
    # FALTA GUARDAR EL ARCHIVO Y AGREGAR EL BOTON DE DESCARGAR EL COMPROBANTE EXISTENTE
    return redirect(url_for("estudio_estado3", estudio=estudio.id))


def estudio_estado3():
    """seleccion de turno"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    agendados = db.session.query(Estudio.turno).filter(Estudio.turno != None).all()
    # es una lista de datetime

    """with open("archivos/Patologias.csv") as data_set:
        reader = csv.reader(data_set)
        for fila in reader:
            flash(fila[0])
            flash(type(fila))
            db.session.add(DiagnosticoPresuntivo(nombre=fila))
    """
    # ruta = current_app.config["UPLOADED_FACTURAS_DEST"]
    # ruta_archivo = os.path.join(ruta, estudio.archivoConsentimiento)

    # ruta_archivo = "sdfsdf"
    return render_template("estudio/estado3.html", estudio=estudio, agendados=agendados)


def estudio_estado3_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    fecha = request.form["fecha"]
    hora = request.form["hora"]

    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()

    turno = fecha.replace("-", "/") + "-" + hora
    estudio.turno = datetime.strptime(turno, "%Y/%m/%d-%H:%M")
    estudio.estadoActual += 1
    # falta chekear turno disponible

    db.session.commit()
    cargarNuevoEstado(estudio)

    return redirect(url_for("estudio_estado4", estudio=estudio.id))


def estudio_estado4():
    """toma de muestra"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    enfecha = estudio.fecha < datetime.now()
    return render_template("estudio/estado4.html", estudio=estudio, enfecha=enfecha)


def cancelar_turno():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()
    estudio.turno = None
    estudio.estadoActual -= 1

    agendados = db.session.query(Estudio.turno).filter(Estudio.turno != None).all()
    db.session.commit()
    cargarNuevoEstado(estudio)

    return render_template("estudio/estado3.html", estudio=estudio, agendados=agendados)


def estudio_estado4_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    freezer = request.form["freezer"]
    muestra = request.form["muestra"]
    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()

    estudio.muestra_ml = muestra
    estudio.muestra_freezer = freezer

    estudio.estadoActual += 1
    db.session.commit()
    cargarNuevoEstado(estudio)

    return redirect(url_for("estudio_estado5", estudio=estudio.id))


def estudio_estado5():
    """retiro de muestra"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    return render_template("estudio/estado5.html", estudio=estudio)


def estudio_estado5_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    empleado = request.form["empleado"]
    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()

    estudio.empleadoMuestra = empleado
    estudio.estadoActual += 1
    db.session.commit()
    cargarNuevoEstado(estudio)
    return redirect(url_for("estudio_estado6", estudio=estudio.id))


def estudio_estado6():
    """esperando formar lote"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    return render_template("estudio/estado6.html", estudio=estudio)


def estudio_estado7():
    """esperando formar lote"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    return render_template("estudio/estado7.html", estudio=estudio)


def estudio_estado8():
    """esperando formar lote"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()

    return render_template("estudio/estado8.html", estudio=estudio)


def estudio_estado8_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    informe = request.form["informe"]
    valor = request.form["resultado"]

    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()

    resultado = Resultado(int(valor), informe)
    db.session.add(resultado)
    db.session.commit()
    estudio.resultado_id = resultado.id
    estudio.estadoActual += 1

    db.session.commit()
    cargarNuevoEstado(estudio)

    return redirect(url_for("estudio_estado9", estudio=estudio.id))
    # return render_template("estudio/estado8.html", estudio=estudio)


def estudio_estado9():
    """envio de mail"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()
    resultado = Resultado.query.filter(Resultado.id == estudio.resultado_id).first()
    medico = MedicoDerivante.query.filter(
        MedicoDerivante.id == estudio.medicoDerivante
    ).first()

    return render_template(
        "estudio/estado9.html", estudio=estudio, resultado=resultado, medico=medico
    )


def estudio_estado9_carga():
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    id_estudio = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == id_estudio).first()
    estudio.resultadoEnviado = True
    estudio.estadoActual += 1

    db.session.commit()
    cargarNuevoEstado(estudio)
    return redirect(url_for("estudio_estado10", estudio=estudio.id))


def estudio_estado10():
    """fin"""
    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    estudio_id = request.args.get("estudio")
    estudio = Estudio.query.filter(Estudio.id == estudio_id).first()
    resultado = Resultado.query.filter(Resultado.id == Estudio.resultado_id).first()

    return render_template(
        "estudio/estado10.html", estudio=estudio, resultado=resultado
    )


def download():
    filename = request.args.get("filename")
    ruta = current_app.config["UPLOADED_FACTURAS_DEST"]
    return send_from_directory(ruta, filename, environ=request.environ)


def actualizar():

    if not authenticated(session):
        abort(401)
    if not (session["rol"] == 2):
        abort(401)

    import datetime

    estudios = Estudio.query.all()

    for estudio in estudios:
        if estudio.estadoActual == 1:
            fecha = datetime.datetime.today() - datetime.timedelta(days=30)
            if estudio.fecha < fecha:
                estudio.anulado = True
                estudio.estadoActual = -1
                db.session.commit()
        else:
            if (
                estudio.estadoActual >= 5
                and estudio.estadoActual <= 9
                and not estudio.retrasado
            ):
                fecha = datetime.datetime.today() - datetime.timedelta(days=90)
                if estudio.turno < fecha:
                    estudio.retrasado = True
                    db.session.commit()

    return redirect(url_for("estudio_index"))


def retrasados_index():
    """listado de estudios retrasados"""

    if not authenticated(session):
        abort(401)

    if not (session["rol"] == 2):
        abort(401)

    estudios = (
        db.session.query(Estudio, Paciente, TipoEstudio)
        .filter(Estudio.retrasado == True)
        .filter(Estudio.paciente == Paciente.id)
        .filter(Estudio.tipoEstudio == TipoEstudio.id)
        .all()
    )

    return render_template("estudio/retrasados.html", estudios=estudios)
