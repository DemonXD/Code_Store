import jinja2
import asyncio
import aiohttp_jinja2
from collections import Counter
from .models import Person
from db import db
from aiohttp import web, WSMsgType
from aiohttp.web import Request, Response, json_response
from playhouse.shortcuts import model_to_dict
from playhouse.signals import post_save
from syncer import sync


async def index(request):
    return aiohttp_jinja2.render_template(
        "index.html",
        request,
        context={}
    )

async def greet_user(request):
    data = await request.json()
    if Counter(list(data.keys())) == Counter(["name", "lastname"]):
        with db.atomic() as transaction:  # Opens new transaction.
            try:
                person = Person.create(name=data['name'],lastname=data['lastname'])
            except Exception as e:
                transaction.rollback()
                return json_response({"code": 4000, "msg": f"{e}", "data": ""}, status=400)
            return json_response({"code": 2000, "msg": "OK", "data": model_to_dict(person)}, status=200)
    else:
        return json_response({"code": 4001, "msg": "create user error, paras wrong!", "data": ""}, status=401)


async def getAll(request):
    try:
        person_list = [model_to_dict(x) for x in Person.getAll()]
    except AssertionError:
        return json_response({"code": 4000, "msg": "no person in database", "data":""}, status=400)
    return json_response({"code": 2000, "msg": "OK", "data":person_list}, status=200)


async def getByName(request):
    name = request.match_info.get("name", "Error")
    if name != "Error":
        try:
            person = Person.getByName(name)
        except AssertionError:
            return json_response({"code": 4000, "msg": f"no {name} in database", "data": ""}, status=400)
        return json_response({"code": 2000, "msg": "OK", "data": model_to_dict(person)})


async def websocket_handler(request):
    resp = web.WebSocketResponse()
    available = resp.can_prepare(request)

    await resp.prepare(request)
    await resp.send_str('Welcome!!!')

    try:
        loop = request.app['loop']
        # request.app['async_tasks'].append(loop.create_task(pushdata(resp)))
        async for msg in resp:
            if msg.type == web.WSMsgType.TEXT:
                pass
            else:
                return resp
        return resp

    finally:
        print('Someone disconnected.')

@post_save(sender=Person)
def trigger_push_data(sender, instance, created):
    print(model_to_dict(instance))


# async def pushdata(ws):
#     count = 0
#     loop = asyncio.get_running_loop()
#     while True:
#         count += 1
#         await ws.send_str(f"{count}")
#         await asyncio.sleep(2, loop=loop)
