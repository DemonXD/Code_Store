from configure import db as dbs
from peewee import Model


def CreatedTable(table) -> int:
    print(f'测试{table}是否被创建')
    table_name = table._meta.__dict__.get('db_table')
    result = dbs.execute_sql(
        f"select count(*) from pg_class where relname = '{table_name}';"
    )
    count = result.fetchone()
    print(f'{table}-->{count}')
    return count[0]


def CreateTable(table) -> None:
    if CreatedTable(table) == 0:
        print(f'{table}将会被创建')
        table.create_table()
        print(f'{table}理论上创建成功')
    return None

def jsonify(records):
    """
    Parse asyncpg record response into JSON format
    """
    list_return = []
    for r in records:
        itens = r.items()
        list_return.append({i[0]: i[1].rstrip() if type(
            i[1]) == str else i[1] for i in itens})
    return list_return
