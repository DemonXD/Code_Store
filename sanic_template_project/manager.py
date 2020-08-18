import settings
import os
import click
import inspect
import sys
from configure import db as dbs
from apps import app
from CustomerException import ParameterError
from apps.API.models import (
    Model,
    Device,
    DeviceService,
    DeviceServiceData
)
from asyncpg import create_pool
from utils.table_util import CreateTable


###########################################
########对于非orm项目可以取消注释下############
########面两行用于全局引用数据库连 ############
########接池                   ############
###########################################

# @app.listener('before_server_start')
# async def register_db(app, loop):
# conn = "postgres://{user}:{password}@{host}:{port}/{database}".format(
#     user=settings.CONFIG.DB_USER, password=settings.CONFIG.DB_PASSWORD,
#     host=settings.CONFIG.DB_HOST, port=settings.CONFIG.DB_PORT,
#     database=settings.CONFIG.DB_DATABASE
# )
# app.settings['pool'] = await create_pool(
#     dsn=conn,
#     min_size=10,
#     max_size=10,
#     max_queries=50000,
#     max_inactive_connection_lifetime=300,
#     loop=loop
# )

# @app.listener('after_server_stop')
# async def close_connection(app, loop):
#     pool = app.settings['pool']
#     async with pool.acquire() as conn:
#         await conn.close()



@app.listener('before_server_start')
async def register_db(app, loop):
    pass


@click.group()
def run():
    pass


@click.command()
@click.argument('db')
def init(db):
    # 如何分析models下所有自建的Model，然后自动对其进行建表操作，
    # 目前可以获得models下所有的class，包括import的
    try:
        if db == 'db':
            __import__('apps.API.models')
            modules = sys.modules['apps.API.models']
            for name, obj in inspect.getmembers(modules, inspect.isclass):
                if 'apps.API.models' in str(obj):
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    CreateTable(obj)
                    sys.stdout.write('OK')
                    sys.stdout.flush()

        else:
            raise ParameterError("Parameter Error, Please use 'db'!")
    except ParameterError as e:
        print(e)
        e = None


@click.command()
def shell():
    os.system('ipython -i -m "apps.models"')


@click.command()
def runserver():
    app.run(host="0.0.0.0", port=8001, workers=4)


run.add_command(init)
run.add_command(shell)
run.add_command(runserver)


if __name__ == "__main__":
    # app.settings.ACCESS_LOG = False
    run()
