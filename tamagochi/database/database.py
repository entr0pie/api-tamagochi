from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine("mysql+pymysql://root:root@mariadb/Tamagochi")

Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parent'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    password = Column(String)
    gender = Column(String)

class Child(Base):
    __tablename__ = 'children'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    access_token = Column(String)
    balance = Column(Integer)
    gender = Column(String)
    id_parent_fk = Column(Integer, ForeignKey('parent.id'))

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    period = Column(Integer)
    frequency = Column(String)
    is_visible = Column(Integer)
    id_parent_fk = Column(Integer, ForeignKey('parent.id'))

def create_session():
    Session = sessionmaker(bind=engine)
    return Session()

