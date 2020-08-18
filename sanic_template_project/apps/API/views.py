from collections import Counter
from sanic import request, Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json, file, html
from asyncpg.exceptions import *
from playhouse.shortcuts import model_to_dict
from .models import (
    Device,
    DeviceService,
    DeviceServiceData
)
from configure import db

class DeviceView(HTTPMethodView):
    async def get(self, request):
        alls = Device.select()
        print([model_to_dict(x) for x in alls])
        return json({"": ""}, status=200)

    @db.atomic()
    async def post(self, request):
        data = request.json
        if Counter(list(data.keys())) == Counter([
                        "ipaddress",
                        "username",
                        "password",]):

            Device.create(ipaddress=data['ipaddress'],
                        username=data['username'],
                        password=data['password'])
            one = Device.filter(username=data['username']).first()

            return json({"code": 2001, "data": model_to_dict(one)},status=200) 


