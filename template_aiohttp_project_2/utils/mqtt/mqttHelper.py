import imp
import json
import paho.mqtt.client as mqtt
from config.PubManager import PublicManager


class MQTTSubscriber(mqtt.Client):
    log = None
    __client = None

    def on_log(self, client, userdata, level, buf):
        pass
        # self.log(logger.level, buf)

    def on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            PublicManager.logger.error("Connected Fail, result code %d", rc)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        # data_logger.info("SUB %s <== %s", payload, msg.topic)
        # logger.debug("SUB %s <== %s", payload, msg.topic)

        event_dict = json.loads(payload)
        pass


    def start(self, username=None, password=None, host=None, port=1883, topic=None):
        """
        启动MQTT订阅监听
        :param username:    用户名
        :param password:    密码
        :param host:        MQTT主机地址
        :param port:        端口
        :param topic:       订阅主题
        :return:
        """
        self.username_pw_set(username, password)
        self.connect(host, port, 60)
        self.subscribe(topic, qos=1)
        PublicManager.logger.info("Connected to server(%s:%d) successfully,subscribing on '%s'", host, port, topic)

        MQTTSubscriber.__client = self

        self.loop_start()

    @staticmethod
    def pub_msg(topic, msg):
        MQTTSubscriber.__client.publish(topic, msg, 1)
        # logger.debug("PUB %s ==> %s ", msg, topic)
