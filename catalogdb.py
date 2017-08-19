# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Creating the tables User, Cities and Items. In the last one, all the
# attractions are stored
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Cities(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # creating an method for the JSON-API
    @property
    def serialize(self):
        return{
                'id': self.id,
                'name': self.name
                }


class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String(400), nullable=False)
    category_id = Column(Integer, ForeignKey('cities.id'))
    categories = relationship(Cities)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # creating a method for the json-API
    @property
    def serialize(self):
        return{
                'cat_id': self.category_id,
                'description': self.description,
                'id': self.id,
                'title': self.name,
                }

engine = create_engine('sqlite:///citiesfinal.db')

Base.metadata.create_all(engine)
