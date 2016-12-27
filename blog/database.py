from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from . import app
from flask_login import UserMixin

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)

class User(Base):
	__tablename__= "users"

	id = Column(Integer, primary_key=True)
	name = Column(String(128))
	email = Column(String(128), unique=True)
	password = Column(String(128))
	is_active = Column(Boolean, default=True)

Base.metadata.create_all(engine)