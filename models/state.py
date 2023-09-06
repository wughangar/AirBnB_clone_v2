#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    if 'HBNB_TYPE_STORAGE' in os.environ and \
            os.environ['HBNB_TYPE_STORAGE'] == 'db':
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """
            this getter attribute retursn the list of city intances
            """
            from models import storage
            cityList = []
            for city_id, city in storage.all(City).items():
                if city.state_id == self.id:
                    cityList.append(city)
            return cityList
