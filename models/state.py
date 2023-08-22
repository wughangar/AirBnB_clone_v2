#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    if models.storage_type == 'db':
        cities = relationship("City",
                              backref="state",
                              cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """
            this getter attribute retursn the list of city intances
            """
            cityList = []
            for city_id, city in models.storage.all(City).items():
                if city.state_id == self.id
                cityList.append(city)
            return cityList
