from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    BigInteger
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()
