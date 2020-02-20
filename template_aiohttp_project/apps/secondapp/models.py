from db import BaseModel
from peewee import CharField, IntegerField, DateTimeField


class Engineer(BaseModel):
    name = CharField(max_length=12, unique=True)
    lastname = CharField(max_length=12)

    @staticmethod
    def getByName(name):
        pass

    @staticmethod
    def getAll():
        pass

    @staticmethod
    def getLast():
        pass


class Voltage(BaseModel):
    value = IntegerField()

