from db import BaseModel
from peewee import CharField, IntegerField, DateTimeField


class Person(BaseModel):
    name = CharField(max_length=12, unique=True)
    lastname = CharField(max_length=12)

    @staticmethod
    def getByName(name):
        person = Person.select().where(Person.name == name).first()
        assert person != None
        return person

    @staticmethod
    def getAll():
        persons = Person.select()
        assert len(persons) != 0
        return persons

    @staticmethod
    def getLast():
        person = Person.select().order_by(Person.id.desc()).first()
        assert person != None
        return person


class Temperature(BaseModel):
    value = IntegerField()
