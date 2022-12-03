from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Tournament(Base):

    __tablename__ = 'tournament'

    id = Column(Integer(), primary_key=True)
    name = Column(String(128))


class ComandEvent(Base):

    __tablename__ = 'command_event'

    id = Column(Integer(), primary_key=True)
    home_player = Column(String(128))
    away_player = Column(String(128))
    home_score = Column(Integer())
    away_score = Column(Integer())
    type = Column(String(128))
    date = Column(Date)
    league_id = Column(ForeignKey("tournament.id"))


class MotorsportCategory(Base):

    __tablename__ = 'motorsport_category'

    id = Column(Integer(), primary_key=True)
    name = Column(String(128))


class MotorSport(Base):

    __tablename__ = 'motorsport'

    id = Column(Integer(), primary_key=True)
    name = Column(String(128))
    type = Column(String(128))
    category_id = Column(ForeignKey("motorsport_category.id"))
