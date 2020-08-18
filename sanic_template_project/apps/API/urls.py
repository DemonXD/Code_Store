from apps.API import api
from .views import DeviceView

api.add_route(DeviceView.as_view(), "/device/")