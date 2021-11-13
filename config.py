from os import environ


class Config(object):
    """Base configuration."""

    DB_HOST = "bd_name"
    DB_USER = "db_user"
    DB_PASS = "db_pass"
    DB_NAME = "db_name"
    SECRET_KEY = "secret"

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class ProductionConfig(Config):
    """Production configuration."""

    DB_HOST = environ.get("DB_HOST", "ec2-44-198-236-169.compute-1.amazonaws.com")
    DB_USER = environ.get("DB_USER", "lnilfufdgovfrz")
    DB_PASS = environ.get(
        "DB_PASS", "025ad4b0aa98fec334d6b3ad1659ce2f139ccffacdb613447c4425195fcf7eab"
    )
    DB_NAME = environ.get("DB_NAME", "dfg898rc4rdfkl")
    DB_PORT = environ.get("DB_PORT", "5432")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class DevelopmentConfig(Config):
    """Development configuration."""

    UPLOAD_FOLDER = "/tmp"
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")
    DB_PORT = environ.get("DB_PORT", "3306")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    # sqlalchemy no usa por defecto pymysql, agregando estas sentencias, yo le digo que se conecte a mi base de datos


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")


config = dict(
    development=DevelopmentConfig, test=TestingConfig, production=ProductionConfig
)

# More information
# https://flask.palletsprojects.com/en/2.0.x/config/
