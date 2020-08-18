from peewee import (
    SqliteDatabase, Model, CharField,
    IntegerField, DateTimeField
)
from playhouse.sqlite_ext import JSONField
from datetime import datetime
from faker import Faker

fake = Faker(locale='zh_CN')
db = SqliteDatabase("test.db")

def row2dict(row):
    return row.__dict__['__data__'] 


class BaseModel(Model):
    class Meta:
        database = db


class Resource(BaseModel):
    url = CharField(max_length=255)
    method = CharField(max_length=12) # GET, PUT, POST, DELETE

    @staticmethod
    def has_resource(resource: str, method: str) -> bool:
        db.connect()
        try:
            resource = Resource.select().where(
                Resource.url == resource, Resource.method == method).get()
        except Resource.DoesNotExist as e:
            db.close()
            return False
        db.close()
        return True


class Employer(BaseModel):
    name = CharField(max_length=64)
    mobile = CharField(max_length=14)
    position = CharField(default="Employer")
    email = CharField(max_length=64)

    @staticmethod
    def get_all_employer():
        db.connect()
        alls = [each for each in Employer.select()]
        db.close()
        return alls

    @staticmethod
    def get_all_employer_dict():
        return [row2dict(row) for row in Employer.get_all_employer()]
    
class approvalTask(BaseModel):
    name = CharField(max_length=255)
    approvallink = JSONField(null=False)


def init_tables():
    db.connect()
    db.create_tables([Employer, approvalTask, Resource])
    if len(Employer.select()) > 0:
        pass
    else:
        fake_employers()
    db.close()

def fake_employers():
    for _ in range(10):
        Employer(
            name=fake.name_male(),
            mobile=fake.phone_number(),
            position="职员",
            email=fake.email()).save()