from sqlalchemy import Column, Integer, String, JSON, UniqueConstraint
from .Base import Base

class Documents(Base):
    __tablename__ = 'T001_Documents'

    document_id = Column(Integer, primary_key=True)
    artikelnummer = Column(String(255), nullable=False)
    hauptpackvorschrift = Column(String(255), nullable=False)
    data = Column(JSON)

    __table_args__ = (
        UniqueConstraint('artikelnummer', 'hauptpackvorschrift', name='_artikelnummer_hauptpackvorschrift_uc'),
        {'schema': 'dsd'},
    )

    def __repr__(self):
        return f"<Document(document_id='{self.document_id}', artikelnummer='{self.artikelnummer}', hauptpackvorschrift='{self.hauptpackvorschrift}')>"