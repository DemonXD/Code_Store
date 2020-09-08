import aiohttp_cors
from handlers.http_handler import handle
from handlers.ws_handler import wshandle


def init_urls(app):
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
    })
    cors.add(app.router.add_get("/ping", handle))
    cors.add(app.router.add_get("/echo", wshandle))
    return app