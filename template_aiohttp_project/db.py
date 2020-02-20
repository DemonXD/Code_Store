from peewee_async import PooledPostgresqlDatabase
from peewee import Model
from playhouse.signals import Model as sModel
from utils.async_sqlite import SqliteDatabase
import settings

if settings.CONFIG.DB_BACKEND == "sqlite":
    db = SqliteDatabase("test.db")
elif settings.CONFIG.DB_BACKEND == "postgresql":
    db = PooledPostgresqlDatabase(
        user=settings.CONFIG.DB_USER,
        password=settings.CONFIG.DB_PASSWORD,
        host=settings.CONFIG.DB_HOST,
        database=settings.CONFIG.DB_DATABASE
    )
else:
    raise ValueError("db backend error! sqlite or postgredql!")

# class BaseModel(Model):
#     class Meta:
#         database = db

class BaseModel(sModel):
    class Meta:
        database = db