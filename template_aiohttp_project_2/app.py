from aiohttp import web
from settings import PublicManager
from urls import init_urls


async def before_app_run(app):
    pass


async def after_app_stop(app):
    pass


def init_app():
    app = web.Application()
    init_urls(app)
    app.on_startup.append(before_app_run)
    app.on_shutdown.append(after_app_stop)
    return app

if __name__=="__main__":
    try:
        app = init_app()
        PublicManager.conf.read_master()
        web.run_app(
            app,
            host=PublicManager.conf.host,
            port=PublicManager.conf.port
        )

    except KeyboardInterrupt:
        pass
