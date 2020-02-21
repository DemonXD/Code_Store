import settings
# from peewee_async import PooledPostgresqlDatabase
from peewee import Model, SqliteDatabase, PostgresqlDatabase
from playhouse.signals import Model as sModel
# from utils.async_sqlite import SqliteDatabase
from utils.mqtt_subscriber import MQTTSubscriber
from peewee_migrate import Router

if settings.CONFIG.DB_BACKEND == "sqlite":
    db = SqliteDatabase("test.db")
    migrate_router = Router(db)
elif settings.CONFIG.DB_BACKEND == "postgresql":
    # db = PooledPostgresqlDatabase(
    db = PostgresqlDatabase(
        user=settings.CONFIG.DB_USER,
        password=settings.CONFIG.DB_PASSWORD,
        host=settings.CONFIG.DB_HOST,
        database=settings.CONFIG.DB_DATABASE
    )
    migrate_router = Router(db)
else:
    raise ValueError("db backend error! sqlite or postgredql!")

# class BaseModel(Model):
#     class Meta:
#         database = db

class BaseModel(sModel):
    class Meta:
        database = db


async def start_mqtt(app):
    app['mqtt_client'] = mqtt_client = MQTTSubscriber()
    mqtt_client.start(
        os.environ.get('MQTT_USERNAME'),
        os.environ.get('MQTT_PASSWORD'),
        os.environ.get('MQTT_HOST'),
        int(os.environ.get('MQTT_PORT')),
        os.environ.get('MQTT_TOPIC')
    )
