import os
from os import path, environ
from os.path import abspath, dirname, join
from flask import Flask, render_template, g, Blueprint
from flask_session import Session
from config import config
from app import db
from app.resources import (
    empleado,
    estudio,
    estudio_paciente,
    lote,
    liquidacionExtracciones,
    paciente,
    reportes,
)
from app.resources import auth
from app.resources import configuracion
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.helpers import config as helper_config
import logging


logging.basicConfig()  # logging basico para ver querys que ejecuta mi app
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"  # para guardar la sesion
    Session(app)

    # Define the application directory
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    # APP_FILES = os.makedirs(os.path.join(APP_ROOT, "archivos"), exist_ok=True)
    APP_FILES = os.path.join(APP_ROOT, "archivos")
    APP_FACTURAS = os.path.join(APP_FILES, "facturas")
    app.config["UPLOADED_FILES_DEST"] = APP_FILES
    app.config["UPLOADED_FACTURAS_DEST"] = APP_FACTURAS

    os.makedirs(APP_FILES, exist_ok=True)
    os.makedirs(APP_FACTURAS, exist_ok=True)

    """app.config["UPLOADED_FACTURAS_DEST"] = os.makedirs(
        os.path.join(app_files, "facturas"), exist_ok=True
    )"""

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Media dir
    # os.makedirs(os.path.join(app.instance_path, "archi"), exist_ok=True)

    # Configure db
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(global_settings=helper_config.check_config)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule(
        "/iniciar_sesion_paciente", "auth_loginPaciente", auth.loginPaciente
    )
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )
    app.add_url_rule(
        "/autenticacionPaciente",
        "auth_authenticatePaciente",
        auth.authenticatePaciente,
        methods=["POST"],
    )
    app.add_url_rule(
        "/paciente/registrarme", "nuevoPaciente", paciente.registrarPaciente
    )
    app.add_url_rule(
        "/registrarPaciente",
        "registrarPaciente",
        paciente.registro_paciente,
        methods=["POST"],
    )

    # Rutas del Configurador
    app.add_url_rule("/configurador", "configurador_home", configuracion.index)
    app.add_url_rule(
        "/configurador/editar",
        "configurador_edit",
        configuracion.configurar,
        methods=["POST"],
    )

    # Rutas de Admin
    app.add_url_rule("/admin", "empleado_index", empleado.index)
    app.add_url_rule("/admin", "empleado_create", empleado.create, methods=["POST"])
    app.add_url_rule("/admin/nuevo", "empleado_new", empleado.new)
    app.add_url_rule(
        "/admin/update", "empleado_update", empleado.update, methods=["POST"]
    )
    app.add_url_rule("/admin/edit", "empleado_edit", empleado.edit)

    app.add_url_rule("/admin/switchstate", "empleado_swichtstate", empleado.swichtstate)

    # Rutas de Empleado
    app.add_url_rule("/empleado", "empleado_home", estudio.listar)
    app.add_url_rule("/empleado/estudios", "estudio_index", estudio.index)
    app.add_url_rule(
        "/empleado/estudios/actualizarEstados", "estudio_actualizar", estudio.actualizar
    )
    app.add_url_rule("/empleado/estudios/ver_estudio", "estudio_ver", estudio.ver)
    app.add_url_rule(
        "/paciente/estudios/ver_estudio", "paciente_estudio_ver", estudio_paciente.ver
    )

    # estudio estado 0
    app.add_url_rule("/empleado/nuevo_estudio", "estudio_new", estudio.new_estudio)
    app.add_url_rule(
        "/empleado/nuevo_estudio",
        "estudio_create",
        estudio.create_estudio,
        methods=["POST"],
    )
    app.add_url_rule("/empleado/nuevo_paciente", "paciente_new", paciente.new_paciente)
    app.add_url_rule(
        "/empleado/nuevo_paciente",
        "paciente_create",
        paciente.create_paciente,
        methods=["POST"],
    )
    app.add_url_rule("/paciente", "paciente_home", estudio_paciente.misEstudios)

    app.add_url_rule(
        "/empleado/edit_paciente",
        "paciente_editar",
        paciente.update_paciente,
        methods=["POST"],
    )
    app.add_url_rule(
        "/empleado/edit_paciente",
        "paciente_update",
        paciente.editar_paciente,
        methods=["GET"],
    )
    app.add_url_rule(
        "/paciente/edit_perfil",
        "paciente_editar_perfil",
        paciente.update_perfil,
        methods=["POST"],
    )

    app.add_url_rule("/empleado/pacientes", "paciente_index", paciente.index)

    # estudios para crear Lote
    app.add_url_rule(
        "/lotes/formarLote",
        "estudiosFormarLote_index",
        lote.estudiosFormarLote_index,
    )

    app.add_url_rule(
        "/lotes/formarLote/nuevo",
        "estudiosParaCrearLote_formarLote",
        lote.formarLote,
        methods=["POST"],
    )

    app.add_url_rule(
        "/lotes/lotesEnProcesamiento",
        "lote_enProcesamiento_index",
        lote.esperaURL_index,
    )

    app.add_url_rule(
        "/lotes/verEstudios", "lote_enProcesamiento_verEstudios", lote.verEstudios
    )

    app.add_url_rule(
        "/lotes/lotesEnProcesamiento/URL",
        "lote_enProcesamiento_agregarURL",
        lote.agregarURL,
        methods=["POST"],
    )

    app.add_url_rule(
        "/lotes/lotesProcesados",
        "lote_procesado_index",
        lote.procesados_index,
    )

    # liquidacion de extracciones
    app.add_url_rule(
        "/liquidacion_Extracciones",
        "liquidacionExtracciones_index",
        liquidacionExtracciones.index,
    )
    app.add_url_rule(
        "/liquidacion_Extracciones/Abonar",
        "liquidacionExtracciones_abonar",
        liquidacionExtracciones.abonar,
        methods=["POST"],
    )

    # reportes
    app.add_url_rule(
        "/reporte_boxplot",
        "reporte_boxplot",
        reportes.boxPlot,
    )
    app.add_url_rule("/reportes/cantTipo", "reportes_tipo", reportes.cantTipo)
    app.add_url_rule("/reportes/cantMes", "reportes_mes", reportes.cantMes)

    # estudio estado 1
    app.add_url_rule("/empleado/estudio1", "estudio_estado1", estudio.estudio_estado1)
    app.add_url_rule(
        "/empleado/validarComprobante", "validarComprobante", estudio.validarComprobante
    )
    app.add_url_rule(
        "/empleado/estudio1",
        "estudio_estado1_carga",
        estudio.estudio_estado1_carga,
        methods=["POST"],
    )
    app.add_url_rule(
        "/paciente/estudio1",
        "paciente_estudio_estado1",
        estudio_paciente.estudio_estado1,
    )
    app.add_url_rule(
        "/paciente/estudio1",
        "paciente_estudio_estado1_carga",
        estudio_paciente.estudio_estado1_carga,
        methods=["POST"],
    )

    app.add_url_rule("/empleado/estudio2", "estudio_estado2", estudio.estudio_estado2)
    app.add_url_rule(
        "/empleado/estudio2",
        "estudio_estado2_carga",
        estudio.estudio_estado2_carga,
        methods=["POST"],
    )

    app.add_url_rule(
        "/paciente/estudio2",
        "paciente_estudio_estado2",
        estudio_paciente.estudio_estado2,
    )
    app.add_url_rule(
        "/paciente/estudio2",
        "paciente_estudio_estado2_carga",
        estudio_paciente.estudio_estado2_carga,
        methods=["POST"],
    )

    app.add_url_rule("/empleado/estudio3", "estudio_estado3", estudio.estudio_estado3)
    app.add_url_rule(
        "/empleado/estudio3",
        "estudio_estado3_carga",
        estudio.estudio_estado3_carga,
        methods=["POST"],
    )

    app.add_url_rule(
        "/paciente/estudio3",
        "paciente_estudio_estado3",
        estudio_paciente.estudio_estado3,
    )
    app.add_url_rule(
        "/paciente/estudio3",
        "paciente_estudio_estado3_carga",
        estudio_paciente.estudio_estado3_carga,
        methods=["POST"],
    )

    app.add_url_rule("/empleado/estudio4", "estudio_estado4", estudio.estudio_estado4)
    app.add_url_rule(
        "/empleado/cancelarturno", "cancelar_turno", estudio.cancelar_turno
    )
    app.add_url_rule(
        "/paciente/cancelarturno",
        "paciente_cancelar_turno",
        estudio_paciente.cancelar_turno,
    )
    app.add_url_rule(
        "/empleado/estudio4",
        "estudio_estado4_carga",
        estudio.estudio_estado4_carga,
        methods=["POST"],
    )
    app.add_url_rule(
        "/paciente/estudio4",
        "paciente_estudio_estado4",
        estudio_paciente.estudio_estado4,
    )

    app.add_url_rule("/empleado/estudio5", "estudio_estado5", estudio.estudio_estado5)
    app.add_url_rule(
        "/empleado/estudio5",
        "estudio_estado5_carga",
        estudio.estudio_estado5_carga,
        methods=["POST"],
    )
    app.add_url_rule("/empleado/estudio6", "estudio_estado6", estudio.estudio_estado6)
    app.add_url_rule("/empleado/estudio7", "estudio_estado7", estudio.estudio_estado7)
    app.add_url_rule("/empleado/estudio8", "estudio_estado8", estudio.estudio_estado8)
    app.add_url_rule(
        "/empleado/estudio8",
        "estudio_estado8_carga",
        estudio.estudio_estado8_carga,
        methods=["POST"],
    )
    app.add_url_rule(
        "/empleado/estudio9",
        "estudio_estado9_carga",
        estudio.estudio_estado9_carga,
        methods=["POST"],
    )
    app.add_url_rule("/empleado/estudio9", "estudio_estado9", estudio.estudio_estado9)
    app.add_url_rule(
        "/empleado/estudio10", "estudio_estado10", estudio.estudio_estado10
    )

    app.add_url_rule(
        "/paciente/estudio5",
        "paciente_estudio_estado5",
        estudio_paciente.estudio_estado5,
    )
    app.add_url_rule(
        "/paciente/estudiofin",
        "paciente_estudio_estado10",
        estudio_paciente.estudio_finalizado,
    )

    app.add_url_rule(
        "/empleado/estudios/retrasados", "estudio_retrasado", estudio.retrasados_index
    )

    # Rutas de configuracion
    app.add_url_rule("/descarga", "download", estudio.download)

    # Ruta para el Home (usando decorator)
    app.add_url_rule("/", "home", auth.home)
    """@app.route("/")
    def home():
        return render_template("home.html")"""

    # Rutas de API-REST (usando Blueprints)
    """api = Blueprint("api", __name__, url_prefix="/api")
    api.register_blueprint(issue_api)

    app.register_blueprint(api)"""

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(
        500, handler.internal_error
    )  # Implementar lo mismo para el error 500

    # Retornar la instancia de app configurada
    return app


app = create_app()
