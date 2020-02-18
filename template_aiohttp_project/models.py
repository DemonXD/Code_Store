from db import Base, engine, Session
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    BigInteger
)


class Person(Base):
    __tablename__ = "person"
    # id = Column(String, primary_key=True)
    # name = Column(String)
    name = Column(String, primary_key=True)
    lastname = Column(String)

    @staticmethod
    def getByName(name):
        sess = Session()
        person = sess.query(Person).filter(Person.name == name).first()
        sess.close()
        return person

    @staticmethod
    def getAll():
        sess = Session()
        persons = sess.query(Person).all()
        sess.close()
        return persons

    def save(self):
        sess = Session()
        sess.add(self)
        sess.commit()
        sess.close()

class Temperature(Base):
    __tablename__ = "temp"
    id = Column(BigInteger, primary_key=True)
    value = Column(Integer)


Base.metadata.create_all(engine)
