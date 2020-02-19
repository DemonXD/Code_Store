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

from utils import jsonify


class DeviceView(HTTPMethodView):
    async def get(self, request):
        pass

    async def post(self, request):
        pass
