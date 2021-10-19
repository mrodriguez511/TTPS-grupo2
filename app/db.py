from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app):  # liga nstra app con la bd
    db.init_app(app)
    with app.app_context():
        from app.models.user import User
        from app.models.rol import Rol
    config_db(app)


def config_db(app):
    @app.before_first_request
    def init_database():  # se ejecuta la primera vez con el primer request
        db.create_all()  # a partir de mis modelos crea las tablas en la bd que configure sin valores
        from app import loadData

        loadData.cargarDatos()

    @app.teardown_request  # cuando termina el request, borra la sesion de la base de datos
    def close_session(exception=None):
        db.session.remove()
