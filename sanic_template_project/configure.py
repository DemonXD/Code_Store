from peewee_async import PooledPostgresqlDatabase
from utils.async_sqlite import SqliteDatabase
import settings

# db = PooledPostgresqlDatabase(
#     user=settings.CONFIG.DB_USER,
#     password=settings.CONFIG.DB_PASSWORD,
#     host=settings.CONFIG.DB_HOST,
#     database=settings.CONFIG.DB_DATABASE
# )
db = SqliteDatabase("testasyncsqlite.db")


str = "https://gist.github.com/xsduan/09fb145da3da3a78f5ca844b155f27aa"