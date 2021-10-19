from os import path, environ
from flask import Flask, render_template, g, Blueprint
from flask_session import Session
from config import config
from app import db
from app.resources import user
from app.resources import auth
from app.resources import configuracion
from app.resources import punto_encuentro
#from app.resources.api.issue import issue_api
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.helpers import check as helper_check
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
    app.jinja_env.globals.update(has_permission=helper_check.check_permission)
    app.jinja_env.globals.update(global_settings=helper_config.check_config)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )


    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios/update", "user_update", user.update, methods=["POST"])
    app.add_url_rule("/usuarios/edit", "user_edit", user.edit)
    app.add_url_rule("/usuarios/delete", "user_delete", user.delete, methods=["GET"])
    app.add_url_rule("/usuarios/state", "user_swichtstate", user.swichtstate)

    # Rutas Puntos de encuentro
    app.add_url_rule("/puntoencuentro", "punto_encuentro_index", punto_encuentro.index)
    app.add_url_rule(
        "/puntoencuentro",
        "punto_encuentro_create",
        punto_encuentro.create,
        methods=["POST"],
    )
    app.add_url_rule(
        "/puntoencuentro/nuevo", "punto_encuentro_new", punto_encuentro.new
    )
    app.add_url_rule(
        "/puntoencuentro/update",
        "punto_encuentro_update",
        punto_encuentro.update,
        methods=["POST"],
    )
    app.add_url_rule(
        "/puntoencuentro/edit", "punto_encuentro_edit", punto_encuentro.edit
    )
    app.add_url_rule(
        "/puntoencuentro/delete",
        "punto_encuentro_destroy",
        punto_encuentro.destroy,
        methods=["GET"],
    )
    app.add_url_rule(
        "/puntoencuentro/state",
        "punto_encuentro_swichtstate",
        punto_encuentro.swichtstate,
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
