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

    hostname = CharField(max_length=20, default="raspberry")
    ipaddress = CharField(max_length=15)
    username = CharField(max_length=15)
    password = CharField(max_length=15)
    isadded = BooleanField(default=False)
    status = CharField(max_length=1, default="1")
    flag = BigIntegerField(default=10)
    isremoved = BooleanField(default=False)
    createtime = CharField(max_length=20,
                            default=time.strftime("%Y-%m-%d %H:%M", time.localtime()))
    modifiedtime = CharField(max_length=20,
                              default=time.strftime("%Y-%m-%d %H:%M", time.localtime()))


class DeviceService(Model):
    class Meta:
        database = db

    servicename = CharField(max_length=20)
    commandstarted = BooleanField(default=False)
    runningstatus = CharField(max_length=10, default='error')
    parameters = CharField(max_length=255, default="")
    createtime = CharField(max_length=20,
                            default=time.strftime("%Y-%m-%d %H:%M", time.localtime()))
    modifiedtime = CharField(max_length=20,
                              default=time.strftime("%Y-%m-%d %H:%M", time.localtime()))
    device = ForeignKeyField(Device,
                             related_name="device_services",
                             on_delete="CASCADE")


class DeviceServiceData(Model):
    class Meta:
        database = db

    servicename = CharField(max_length=20)
    servicedata = CharField(max_length=20)
    createtime = CharField(max_length=20,
                            default=time.strftime("%Y-%m-%d %H:%M", time.localtime()))
