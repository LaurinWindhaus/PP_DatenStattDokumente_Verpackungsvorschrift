from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from dotenv import load_dotenv
import os

load_dotenv()

ENVIRONMENT = os.getenv('ENVIRONMENT')

metadata = MetaData(schema='dsd') if ENVIRONMENT == 'PROD' else MetaData()

Base = declarative_base(metadata=metadata)