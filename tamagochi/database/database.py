#!/bin/python3

from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine("sqlite:///database/tamagochi.db")

Base = declarative_base()
Base.metadata.reflect(bind=engine)

class Parent(Base):
    __tablename__ = Base.metadata.tables['parent']

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    password = Column(String)
    gender = Column(String)

class Child(Base):
    __tablename__ = Base.metadata.tables['children']
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    access_token = Column(String)
    balance = Column(Integer)
    gender = Column(String)
    id_parent_fk = Column(Integer, ForeignKey('parent.id'))

def create_session():
    Session = sessionmaker(bind=engine)
    return Session()


