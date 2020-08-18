import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(".env")


class CONFIG:
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # DB Setting (PostgreSQL)
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = int(os.environ.get("DB_PORT"))
    DB_DATABASE = os.environ.get("DB_DATABASE")

    REDIS_BROKER = "127.0.0.1:6379"
    REDIS_RESULT = "127.0.0.1:6379"

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