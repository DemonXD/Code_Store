# from peewee_async import PooledPostgresqlDatabase
from peewee import SqliteDatabase, PostgresqlDatabase
# from utils.async_sqlite import SqliteDatabase
import settings

if settings.CONFIG.DB_BACKEND == "sqlite":
    db = SqliteDatabase("testasyncsqlite.db")
elif settings.CONFIG.DB_BACKEND == "postgresql":
    # db = PooledPostgresqlDatabase(
    db = PostgresqlDatabase(
        user=settings.CONFIG.DB_USER,
        password=settings.CONFIG.DB_PASSWORD,
        host=settings.CONFIG.DB_HOST,
        database=settings.CONFIG.DB_DATABASE
    )
else:
    raise ValueError("db backend error! sqlite or postgredql!")
