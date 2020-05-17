from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()
class Restaurant(Base):
    __tablename__ = 'restaurant'

    restaurant_id = Column(String, primary_key = True)
    food = Column(String)
    name = Column(String)
    location = Column(String)
  
  
  #Add a property decorator to serialize information from this database
    @property
    def serialize(self):

        return {
            'name': self.name,
            'location': self.location,
            'food' : self.food,
            'restaurant_id' : self.restaurant_id
        }

engine = create_engine('sqlite:///restaurants.db')
 

Base.metadata.create_all(engine)