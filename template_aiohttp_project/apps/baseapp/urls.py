from aiohttp.web import RouteTableDef
from .views import (
    index,
    greet_user,
    getAll,
    getByName,
    websocket_handler
)

routers = RouteTableDef()

async def init_routers(app):
    app.router.add_get('/', index)
    app.router.add_post('/createuser/', greet_user)
    app.router.add_get('/getalluser/', getAll)
    app.router.add_get('/getuser/{name}/', getByName)
    app.router.add_get('/test', websocket_handler)