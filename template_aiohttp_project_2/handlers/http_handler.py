from aiohttp.web import json_response
from settings import PublicManager

async def handle(request):
    PublicManager.logger.info("run handle handler")
    return json_response({
                    "code": 200,
                    "data": "pong"
                },
                status=200
            )
