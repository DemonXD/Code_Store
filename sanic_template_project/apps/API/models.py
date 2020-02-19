import time
from peewee import (Model,
                    CharField,
                    BigIntegerField,
                    BooleanField,
                    ForeignKeyField)
from configure import db


class Device(Model):
    class Meta:
        database = db

    id = BigIntegerField(primary_key=True)
    hostname = CharField(max_length=20, default="raspberry")
    ip_address = CharField(max_length=15)
    user_name = CharField(max_length=15)
    password = CharField(max_length=15)
    is_added = BooleanField(default=False)
    status = CharField(max_length=1, default="1")
    flag = BigIntegerField(default=10)
    is_removed = BooleanField(default=False)
    create_time = CharField(max_length=20,
                            default=time.strftime("%Y-%m-%d %H:%M", time.localtime()))
    modified_time = CharField(max_length=20,
                              default=time.strftime("%Y-%m-%d %H:%M", time.localtime()))

    def __str__(self):
        return """{
                "id": {0},
                "hostname": {1},
                "ip_address": {2},
                "user_name": {3},
                "is_added": {4},
                "status": {5},
                "flag": {6},
                "create_time": {7},
                "modified_time": {8},
                }""".format(self.id, self.hostname,
                            self.ip_address, self.user_name,
                            self.is_added, self.status,
                            self.flag, self.create_time,
                            self.modified_time)


class DeviceService(Model):
    class Meta:
        database = db

    id = BigIntegerField(primary_key=True)
    service_name = CharField(max_length=20)
    command_started = BooleanField(default=False)
    running_status = CharField(max_length=10, default='error')
    parameters = CharField(max_length=255, default="")
    create_time = CharField(max_length=20,
                            default=time.strftime("%Y-%m-%d %H:%M", time.localtime()))
    modified_time = CharField(max_length=20,
                              default=time.strftime("%Y-%m-%d %H:%M", time.localtime()))
    device = ForeignKeyField(Device,
                             related_name="device_services",
                             on_delete="CASCADE")

    def __str__(self):
        return """{
                "id": {0},
                "service_name": {1},
                "command_started": {2},
                "running_status": {3},
                "parameters": {4},
                "create_time": {5},
                "modified_time": {6},
                }""".format(self.id, self.service_name,
                            self.command_started, self.running_status,
                            self.parameters, self.create_time,
                            self.modified_time)


class DeviceServiceData(Model):
    class Meta:
        database = db

    id = BigIntegerField(primary_key=True)
    service_name = CharField(max_length=20)
    service_data = CharField(max_length=20)
    create_time = CharField(max_length=20,
                            default=time.strftime("%Y-%m-%d %H:%M", time.localtime()))

    def __str__(self):
        return """{
                "id": {0},
                "service_name": {1},
                "service_data": {2},
                "create_time": {3},
                }""".format(self.id, self.service_name,
                            self.service_data, self.create_time)
