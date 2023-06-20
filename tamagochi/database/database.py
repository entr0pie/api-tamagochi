from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine("mysql+pymysql://root:root@mariadb/Tamagochi")

Base = declarative_base()

class Parent(Base):
    __tablename__ = 'Parent'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    password = Column(String)
    gender = Column(String)

class Child(Base):
    __tablename__ = 'Child'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    access_token = Column(String)
    balance = Column(Integer)
    gender = Column(String)
    parent = Column(Integer, ForeignKey('Parent.id'))

class Task(Base):
    __tablename__ = 'Task'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    period = Column(Integer)
    frequency = Column(String)
    is_visible = Column(Integer)
    parent = Column(Integer, ForeignKey('Parent.id'))

def create_session():
    Session = sessionmaker(bind=engine)
    return Session()

