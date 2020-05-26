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
    state_name = Column(String)
    state_abr = Column(String)
    cities = relationship('City', back_populates="state")
    capital = relationship('State_Capital', back_populates='state')

    def __repr__(self):
        return "<State(state='%s')>" % (self.state_name)


class State_Capital(Base):
    __tablename__ = 'state_capital'
    id = Column(Integer, primary_key=True)
    capital_name = Column(String)
    state_id = Column(Integer, ForeignKey('states.id'))
    state = relationship('State', back_populates="capital")


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    city_name = Column(String)
    state_id = Column(Integer, ForeignKey('states.id'))
    state = relationship('State', back_populates="cities")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
