from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from config import config

db_path = config()
engine = create_engine(db_path)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


class State(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True)
    state = Column(String)
    cities = relationship('City', back_populates="state")


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    state_id = Column(Integer, ForeignKey('states.id'))
    state = relationship('State', back_populates="cities")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
