import jinja2
import aiohttp_jinja2
from collections import Counter
from models import Person
from aiohttp import web, WSMsgType
from aiohttp.web import Request, Response, json_response
from db import Session
from utils import row2dict, pushdata
from sqlalchemy.exc import IntegrityError


async def index(request):
    return aiohttp_jinja2.render_template(
        "index.html",
        request,
        context={}
    )


async def greet_user(request):
    data = await request.json()
    if Counter(list(data.keys())) == Counter(["fname", "lname"]):
        try:
            person = Person(name=data['fname'],lastname=data['lname'])
            persondict = row2dict(person)
            person.save()
            return json_response({"code": 2001, "data": persondict}, status=200)
        except IntegrityError:
            return json_response({"code": 4000, "msg": "name exist"}, status=400)
    else:
        return json_response({"msg": "create user error, paras wrong!"}, status=401)


async def getAll(request):
    person_list = [row2dict(x) for x in Person.getAll()]
    return json_response({"code": 200, "data":person_list}, status=200)


async def getByName(request):

    name = request.match_info.get("name", "Error")
    if name != "Error":
        person = Person.getByName(name)
        return json_response({"code": 200, "data": row2dict(person)})


async def websocket_handler(request):
    resp = web.WebSocketResponse()
    available = resp.can_prepare(request)

    await resp.prepare(request)
    await resp.send_str('Welcome!!!')

    try:
        loop = request.app['loop']
        request.app['async_tasks'].append(loop.create_task(pushdata(resp)))
        async for msg in resp:
            if msg.type == web.WSMsgType.TEXT:
                pass
            else:
                return resp
        return resp

    finally:
        print('Someone disconnected.')
