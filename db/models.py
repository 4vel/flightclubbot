from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, NUMERIC
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import datetime

Base = declarative_base()


class DataAccessLayer:
    """Подключение к базе данных. Сессия"""

    def __init__(self, connection_string):
        self.engine = None
        self.session = None
        self.Session = None
        self.conn_string = connection_string

    def connect(self):
        logging.info(f"Подключаюсь к БД")
        logging.info(self.conn_string)
        self.engine = create_engine(self.conn_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind = self.engine)
        self.session = self.Session()

    def get_session(self):
        logging.info(f"Подключаюсь к БД")
        logging.info(self.conn_string)
        self.engine = create_engine(self.conn_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind = self.engine)
        self.session = self.Session()
        return self.session


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable = False, unique = True, primary_key = True, autoincrement = True)
    created_at = Column(TIMESTAMP, nullable = False, default = datetime.datetime.now())
    updated_at = Column(TIMESTAMP, nullable = False, default = datetime.datetime.now(),
                        onupdate = datetime.datetime.now())

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)

class TableAirportCodes(BaseModel):
    """ Таблица коды аэропортов """

    __tablename__ = 'airports'

    airport_name = Column(VARCHAR())
    airport_code = Column(VARCHAR())
    city_country = Column(VARCHAR())

    def __init__(self, airport_name,  airport_code, city_country):
        self.airport_name = airport_name
        self.airport_code = airport_code
        self.city_country = city_country


    def __repr__(self):
        return f'{self.airport_name} {self.airport_code} {self.city_country}'




class TableUsers(BaseModel):

    """
    Таблица Юзеров
    Нужна для того чтобы обращаться к юзеру по имени
    """

    __tablename__ = 'users'

    user_id = Column(VARCHAR())
    user_name = Column(VARCHAR())

    def __init__(self, user_id,  user_name):
        self.user_id = user_id
        self.user_name = user_name

    def __repr__(self):
        return f'{self.user_id} {self.user_name} '

class TableUserAirports(BaseModel):

    """
    Таблица юзеров и аэропортов
    airport_code - iata
    price - цена в рублях
    """

    __tablename__ = 'destinations'

    user_id = Column(VARCHAR())
    airport_code = Column(VARCHAR())
    price = Column(NUMERIC())

    def __init__(self, user_id,  airport_code, price):
        self.user_id = user_id
        self.airport_code = airport_code
        self.price = price

    def __repr__(self):
        return f'{self.user_id} {self.airport_code} {self.price} '






