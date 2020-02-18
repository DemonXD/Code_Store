import os
import asyncio
import jinja2
import aiohttp_jinja2
from aiohttp import web
from db import Session
from models import Person
from urls import init_routers

async def generate_data():
    while True:
        await asyncio.sleep(2)

async def start_backend_task(app):
    app['loop'] = loop = asyncio.get_event_loop()
    app['generate_data'] = loop.create_task(generate_data())

async def stop_backend_task(app):
    app['generate_data'].cancel()

async def init_app() -> web.Application:
    app = web.Application()
    await init_routers(app)
    app.on_startup.append(start_backend_task)
    app.on_shutdown.append(stop_backend_task)
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
    )
    return app

web.run_app(init_app(), port=10086)