from app.models.configuracion import Configuracion


def check_config():
    return Configuracion.check_config()
