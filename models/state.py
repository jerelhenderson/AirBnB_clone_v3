#!/usr/bin/python3
'''
    Implementation of the State class
'''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    '''
        Implementation for the State.
    '''
    __tablename__ = "states"
    name=""
    # name = Column(String(128), nullable=False)
    # cities = relationship("City", backref="state",
    #                       cascade="all, delete, delete-orphan",
    #                       primaryjoin="City.state.id==State.id")
