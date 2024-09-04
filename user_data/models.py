from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user_data'

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String(10))
    title = Column(String(10))
    first_name = Column(String(100))
    last_name = Column(String(100))
    street = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postcode = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)
    timezone_offset = Column(String(10))
    timezone_description = Column(String(100))
    email = Column(String(255))
    dob_date = Column(DateTime)
    dob_age = Column(Integer)
    registered_date = Column(DateTime)
    registered_age = Column(Integer)
    phone = Column(String(20))
    cell = Column(String(20))
    picture_large = Column(String(255))
    picture_medium = Column(String(255))
    picture_thumbnail = Column(String(255))

    def __repr__(self):
        return f"<User(first_name={self.first_name}, last_name={self.last_name})>"
