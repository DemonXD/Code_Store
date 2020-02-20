import os
import click
import inspect
import sys
import asyncio
import jinja2
import aiohttp_jinja2
import settings
from aiohttp import web
from apps.baseapp.urls import init_routers

async def generate_data():
    while True:
        await asyncio.sleep(2)
        # print("running generate_data")

async def start_backend_task(app):
    app['loop'] = loop = asyncio.get_event_loop()
    app['async_tasks'].append(loop.create_task(generate_data()))

async def stop_backend_task(app):
    [x.cancel() for x in app['async_tasks']]

async def init_app() -> web.Application:
    app = web.Application()
    app['async_tasks'] = []
    await init_routers(app)
    app.on_startup.append(start_backend_task)
    app.on_shutdown.append(stop_backend_task)
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
    )
    return app

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
            for eachapp in settings.INSTALL_APPS:
                models_ = f'{eachapp}.models'
                __import__(models_)
                modules = sys.modules[models_]
                for name, obj in inspect.getmembers(modules, inspect.isclass):
                    if models_ in str(obj):
                        # create table code here
                        obj.create_table(True)
                        sys.stdout.write(f"{name},{str(obj)}, has been created\n")
        else:
            raise ParameterError("Parameter Error, Please use 'db'!")
    except ParameterError as e:
        print(e)
        e = None

@click.command()
def shell():
    strs = ""
    for eachapp in settings.INSTALL_APPS:
        strs += f"from {eachapp}.models import *;"
    print(f'execute order: ipython -i -c "{strs}"')
    os.system(f'ipython -i -c "{strs}"')

@click.command()
def runserver():
    web.run_app(init_app(), port=10086)

run.add_command(init)
run.add_command(shell)
run.add_command(runserver)


if __name__ == "__main__":
    run()