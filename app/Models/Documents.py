from sqlalchemy import Column, Integer, String, JSON, UniqueConstraint, MetaData
from .Base import Base
from dotenv import load_dotenv
import os

load_dotenv()

ENVIRONMENT = os.getenv('ENVIRONMENT', 'DEV')

metadata = MetaData(schema='dsd') if ENVIRONMENT == 'PROD' else MetaData()

class Documents(Base):
    __tablename__ = 'T001_Documents'

    document_id = Column(Integer, primary_key=True)
    artikelnummer = Column(String(255), nullable=False)
    hauptpackvorschrift = Column(String(255), nullable=False)
    data = Column(JSON, default={})

    __table_args__ = (
        UniqueConstraint('artikelnummer', 'hauptpackvorschrift', name='_artikelnummer_hauptpackvorschrift_uc'),
    )

    def __repr__(self):
        return f"<Document(document_id='{self.document_id}', artikelnummer='{self.artikelnummer}', hauptpackvorschrift='{self.hauptpackvorschrift}')>"
    
    def to_dict(self):
        return {
            'document_id': self.document_id,
            'artikelnummer': self.artikelnummer,
            'hauptpackvorschrift': self.hauptpackvorschrift,
            'data': self.data
        }