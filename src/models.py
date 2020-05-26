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

    def get_state(self, state_name):
        state_query = session.query(State). \
                          filter_by(state_name=state_name).first()
        return state_query

    def add_state(self, state_name, state_abr):
        if not self.get_state(state_name):
            session.add(State(state_name=state_name, state_abr=state_abr))
        session.commit()

    def add_state_capital(self, capital_name):
        if not State_Capital().get_state_capital(capital_name):
            session.add(State_Capital(capital_name=capital_name,
                                      state_id=self.id))
        session.commit()


class State_Capital(Base):
    __tablename__ = 'state_capital'
    id = Column(Integer, primary_key=True)
    capital_name = Column(String)
    state_id = Column(Integer, ForeignKey('states.id'))
    state = relationship('State', back_populates="capital")

    def get_state_capital(self, capital_name):
        state_capital_query = session.query(State_Capital). \
                          filter_by(capital_name=capital_name).first()
        return state_capital_query


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    city_name = Column(String)
    state_id = Column(Integer, ForeignKey('states.id'))
    state = relationship('State', back_populates="cities")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
