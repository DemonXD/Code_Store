import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(".env")


INSTALL_APPS = [
    "apps.baseapp",
]


class CONFIG:
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # DB Setting (PostgreSQL)
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = int(os.environ.get("DB_PORT"))
    DB_DATABASE = os.environ.get("DB_DATABASE")

    MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
    MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
    MQTT_HOST = os.environ.get('MQTT_HOST')
    MQTT_PORT = int(os.environ.get('MQTT_PORT'))
    MQTT_TOPIC = os.environ.get('MQTT_TOPIC')

    REDIS_DB = os.environ.get("REDIS_DB")

    # config db type: sqlite / postgresql
    DB_BACKEND = "sqlite"


class DEVELOPMENTCONFIG(CONFIG):
    DEBUG = True


class PRODUCTIONCONFIG(CONFIG):
    DEBUG = False


settings = {
    "dev": DEVELOPMENTCONFIG,
    "prod": PRODUCTIONCONFIG
}