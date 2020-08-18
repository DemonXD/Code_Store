from sanic.views import HTTPMethodView
from sanic.response import json


class pingView(HTTPMethodView):
    def get(self, request):
        return json({"msg":"pong"})