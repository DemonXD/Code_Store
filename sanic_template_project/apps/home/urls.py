from apps.home import home
from .views import pingView

home.add_route(pingView.as_view(), "/ping/")