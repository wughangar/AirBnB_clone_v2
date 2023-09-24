#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship
from models.review import Review


place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column('place_id', String(60), ForeignKey('places.id'),
               primary_key=True, nullable=False),
        Column('amenity_id', String(60), ForeignKey('amenities.id'),
               primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    amenity_ids = []

    reviews = relationship("Review",
                           backref="place",
                           cascade="all, delete-orphan")

    @amenities.setter
    def amenities(self, amenity):
        if isinstance(amenity, Amenity):
            if amenity.id not in self.amenity_ids:
                self.amenity_ids.append(amenity.id)

    amenity_ids = []

    # Define the relationship with Amenity through place_amenity
    amenities = relationship(
        'Amenity',
        secondary=place_amenity,
        viewonly=False,
        back_populates='place_amenities'
    )

    reviews = relationship("Review", backref="place",
                           cascade="all, delete-orphan")
