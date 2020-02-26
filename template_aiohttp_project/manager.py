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
from db import start_mqtt, migrate_router

async def generate_data():
    while True:
        await asyncio.sleep(2)
        # print("running generate_data")

async def start_backend_task(app):
    app['loop'] = loop = asyncio.get_event_loop()
    app['async_tasks'].append(loop.create_task(generate_data()))
    app['async_tasks'].append(loop.create_task(start_mqtt(app)))

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
                try:
                    models_ = f'{eachapp}.models'
                    __import__(models_)
                    modules = sys.modules[models_]
                    for name, obj in inspect.getmembers(modules, inspect.isclass):
                        if models_ in str(obj.__dict__['__module__']):
                            # create table code here
                            obj.create_table(True)
                            sys.stdout.write(f"{name},{str(obj)}, has been created\n")
                except Exception as e:
                    print(e)
                    raise ValueError(f"No Such APP:{eachapp} EXISTED!")
        else:
            raise NameError("Parameter Error, Please use 'db'!")
    except Exception as e:
        print(e)
        e = None

@click.command()
def makemigrations():
    migrate_router.create("allmigrations")

@click.command()
def migrate():
    migrate_router.run()

@click.command()
def shell():
    strs = ""
    for eachapp in settings.INSTALL_APPS:
        strs += f"from {eachapp}.models import *;"
    print(f'execute order: ipython -i -c "{strs}"')
    os.system(f'ipython -i -c "{strs}"')

@click.command()
@click.argument('appname')
def startapp(appname):
    try:
        os.system(f"mkdir -p apps/{appname}")
        os.system(f'touch apps/{appname}/__init__.py')
        os.system(f'touch apps/{appname}/models.py')
        os.system(f'touch apps/{appname}/urls.py')
        os.system(f'touch apps/{appname}/views.py')
    except Exception as e:
        print(e)
        sys.exit(0)


@click.command()
def runserver():
    web.run_app(init_app(), port=10086)

run.add_command(init)
run.add_command(startapp)
# migrations 功能待完善
# run.add_command(makemigrations)
# run.add_command(migrate)
run.add_command(shell)
run.add_command(runserver)


if __name__ == "__main__":
    run()