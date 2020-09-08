import os
from config.config_base import Config
from config.initconf import init_log, init_dbpool, init_mqtt
from config.PubManager import PublicManager


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# config_ini = os.path.join(BASE_DIR, "config.ini")
config_ini = "./config.ini"

# register conf
PublicManager.conf = Config(config_ini)
# init log config
init_log(PublicManager)
# init db config
init_dbpool(PublicManager)
# init mqtt config
init_mqtt(PublicManager)
