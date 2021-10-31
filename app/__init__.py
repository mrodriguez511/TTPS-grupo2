from os import path, environ
from flask import Flask, render_template, g, Blueprint
from flask_session import Session
from config import config
from app import db
from app.resources import empleado, estudio, paciente
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

    # Configure db
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(global_settings=helper_config.check_config)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )

    # Rutas de Admin
    app.add_url_rule("/admin", "empleado_index", empleado.index)
    app.add_url_rule("/admin", "empleado_create", empleado.create, methods=["POST"])
    app.add_url_rule("/admin/nuevo", "empleado_new", empleado.new)
    app.add_url_rule(
        "/admin/update", "empleado_update", empleado.update, methods=["POST"]
    )
    app.add_url_rule("/admin/edit", "empleado_edit", empleado.edit)
    app.add_url_rule(
        "/admin/delete", "empleado_delete", empleado.delete, methods=["GET"]
    )

    # Rutas de Empleado
    app.add_url_rule("/empleado", "estudio_index", estudio.index)

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

    # estudio estado 1
    app.add_url_rule("/empleado/estudio1", "estudio_estado1", estudio.estudio_estado1)
    app.add_url_rule(
        "/empleado/estudio1",
        "estudio_estado1_carga",
        estudio.estudio_estado1_carga,
        methods=["POST"],
    )

    # Rutas de configuracion
    app.add_url_rule("/configuracion", "settings_edit", configuracion.edit)
    app.add_url_rule(
        "/configuracion", "settings_update", configuracion.update, methods=["POST"]
    )

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        return render_template("home.html")

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
