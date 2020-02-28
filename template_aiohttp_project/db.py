import settings
# from peewee_async import PooledPostgresqlDatabase
from peewee import Model, SqliteDatabase, PostgresqlDatabase
from playhouse.signals import Model as sModel
# from utils.async_sqlite import SqliteDatabase
from utils.mqtt_subscriber import MQTTSubscriber
from peewee_migrate import Router
from aioredis import create_pool


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
        settings.CONFIG.MQTT_USERNAME,
        settings.CONFIG.MQTT_PASSWORD,
        settings.CONFIG.MQTT_HOST,
        settings.CONFIG.MQTT_PORT,
        settings.CONFIG.MQTT_TOPIC
    )

async def redis_pool():
    return await create_pool(settings.CONFIG.REDIS_DB)
