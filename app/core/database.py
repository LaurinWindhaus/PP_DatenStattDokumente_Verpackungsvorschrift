from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from models.Base import Base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
ENVIRONMENT = os.getenv('ENVIRONMENT')

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if ENVIRONMENT == "DEV":
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()

def init_db():
    Base.metadata.create_all(engine)