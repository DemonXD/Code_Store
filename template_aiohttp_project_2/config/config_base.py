import configparser

class Config:
    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(self.filename)

    def read_log(self):
        self.level = self.config.get("log", "level")
        self.filepath = self.config.get("log", "filepath")
        self.logname = self.config.get("log", "logname")

    def read_master(self):
        self.host = self.config.get("master", "ip")
        self.port = self.config.get("master", "port")

    def read_mqtt(self):
        self.mqtt_host = self.config.get("mqtt", "host")
        self.mqtt_port = self.config.get("mqtt", "port")
        self.mqtt_topic = self.config.get("mqtt", "topic")
        self.mqtt_username = self.config.get("mqtt", "username")
        self.mqtt_password = self.config.get("mqtt", "password")

    def read_db(self):
        """
        default: PostgreSQL
        """
        self.db_host = self.config.get("db", "host")
        self.db_port = self.config.get("db", "port")
        self.db_name = self.config.get("db", "dbname")
        self.db_user = self.config.get("db", "user")
        self.db_password = self.config.get("db", "password")
        self.db_minconn = self.config.get("db", "minconn")
        self.db_maxconn = self.config.get("db", "maxconn")