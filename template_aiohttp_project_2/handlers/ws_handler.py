from aiohttp.web import (
    WebSocketResponse,
    WSMsgType
)


async def wshandle(request):
    ws = WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.text:
            await ws.send_str("Hello, {}".format(msg.data))
        elif msg.type == WSMsgType.binary:
            await ws.send_bytes(msg.data)
        elif msg.type == WSMsgType.close:
            break

    return ws