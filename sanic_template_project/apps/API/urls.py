from apps.API import api
from .views import indexView, DeviceView

api.add_route(DeviceView.as_view(), "/deivce/")