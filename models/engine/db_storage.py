#!/usr/bin/python3
"""
db storage engine
"""

from models.base_model import Base
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from console import HBNBCommand
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.review import Review


classes = {
        'City': City,
        'Place': Place,
        'State': State,
        'User': User,
        'Amenity': Amenity,
        'Review': Review
        }

class DBStorage:
    """
    initialize db class
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        creating and connecting engine to database
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                     .format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                     pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        query on the current db session
        """
        objs = {}
        if cls:
            query = self.__session.query(cls)
            for obj in query:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objs[key] = obj
        else:
            for cls in classes:
                query = self.__session.query(cls)
                for obj in query:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    objs[key] = obj
        return objs

    def new(self, obj):
        """
        adds the object to curreny database
        """
        self.__session.add(obj)

    def save(self):
        """
        commits all the changes made to db
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes the current database session
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        create all the tables in the database and create the session
        """
        module_name = "models"

        classes = {}
        for name, value in globals().items():
            if isinstance(value, type) and value.__module__ == module_name:
                classes[name] = value
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))
