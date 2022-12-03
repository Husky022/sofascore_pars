import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import sqlalchemy

from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from secrets import DB_NAME, DB_USER, DB_PSWD, DB_HOST, DB_PORT

from .models import Base, Tournament, ComandEvent, MotorsportCategory, MotorSport


# Класс - менеджер по работе с БД
class DBManager:

    def __init__(self):
        self.engine = self.db_engine()
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    @staticmethod
    def db_engine():
        try:
            engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
                                   echo=True)
            engine.connect()
        except sqlalchemy.exc.OperationalError:
            connection = psycopg2.connect(user=DB_USER, password=DB_PSWD)
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            cursor.execute(f'create database {DB_NAME}')
            cursor.close()
            connection.close()
            engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
                                   echo=True)
        return engine

    def close(self):
        self.session.close()

    def commit(self):
        self.session.commit()

    def record_tournaments(self, data):
        self.session.execute(
            insert(Tournament),
            data
        )
        self.commit()

    def record_events(self, data):
        self.session.execute(
            insert(ComandEvent),
            data
        )
        self.commit()

    def record_motor_categories(self, data):
        self.session.execute(
            insert(MotorsportCategory),
            data
        )
        self.commit()

    def record_motorsports(self, data):
        self.session.execute(
            insert(MotorSport),
            data
        )
        self.commit()
