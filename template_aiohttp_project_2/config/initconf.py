import os
import logging
import logging.handlers
from utils.db.dbHelper import DBHelper
from utils.mqtt.mqttHelper import MQTTSubscriber


def init_log(PublicManager):
    PublicManager.conf.read_log()
    PublicManager.logger=logging.getLogger()
    PublicManager.logger.setLevel(PublicManager.conf.level)
   
    fh = logging.handlers.TimedRotatingFileHandler(
        os.path.join(PublicManager.conf.filepath, PublicManager.conf.logname),
        when = 'D',
        # maxBytes=10*1024*1024,
        backupCount = 7 # max 7 days log files
    )

    sh = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s-%(module)s:%(filename)s-L%(levelname)s:%(message)s')
    fh.setFormatter(formatter)
    PublicManager.logger.addHandler(fh)
    PublicManager.logger.addHandler(sh)


def init_dbpool(PublicManager):
    PublicManager.conf.read_db()
    db_config = dict(
        host = PublicManager.conf.db_host,
        port = int(PublicManager.conf.db_port),
        database = PublicManager.conf.db_name,
        user = PublicManager.conf.db_user,
        password = PublicManager.conf.db_password,
        min_size = int(PublicManager.conf.db_minconn),
        max_size = int(PublicManager.conf.db_maxconn)
    )
    PublicManager.dbpool = DBHelper(db_config)


def init_mqtt(PublicManager):
    PublicManager.conf.read_mqtt()
    mqtt_conf = dict(
        host=PublicManager.conf.mqtt_host,
        port=int(PublicManager.conf.mqtt_port),
        topic=PublicManager.conf.mqtt_topic,
        username=PublicManager.conf.mqtt_username,
        password=PublicManager.conf.mqtt_password
    )
    PublicManager.mqttclient = MQTTSubscriber()
    PublicManager.mqttclient.start(**mqtt_conf)