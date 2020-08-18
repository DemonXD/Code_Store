import settings
from sanic import Sanic
from sanic_cors import CORS, cross_origin
from sanic_session import Session
from apps.API.urls import api as api_blueprint
from apps.home.urls import home as home_blueprint


app = Sanic()
Session(app)
CORS(app)
app.config.from_object(settings.settings['dev'])

app.blueprint(api_blueprint)
app.blueprint(home_blueprint)

