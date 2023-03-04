import pathlib
import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

file_ini = pathlib.Path(__file__).parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_ini)

username = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
database_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')
port = config.get('DB', 'PORT')

url = f'postgresql://{username}:{password}@{domain}:{port}/{database_name}'
Base = declarative_base()

engine = create_engine(url, echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
