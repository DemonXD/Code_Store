from configure import db as dbs
from peewee import Model
import settings


def CreatedTable(table) -> int:
    print(f'测试{table}是否被创建')
    table_name = table._meta.__dict__.get('db_table')
    if settings.CONFIG.DB_BACKEND == "postgresql":
        sql = f"select count(*) from pg_class where relname = '{table_name}';"
    elif settings.CONFIG.DB_BACKEND == "sqlite":
        sql = f"select count(*) from sqlite_master where type = 'table' and name = '{table_name}'"
    else:
        raise ValueError("db backend error! sqlite or postgresql!")
    result = dbs.execute_sql(sql)
    count = result.fetchone()
    print(f'{table}-->{count}')
    return count[0]


def CreateTable(table) -> None:
    if CreatedTable(table) == 0:
        print(f'{table}将会被创建')
        table.create_table()
        print(f'{table}理论上创建成功')
    return None


