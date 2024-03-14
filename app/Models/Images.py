from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .Base import Base

class Images(Base):
    __tablename__ = 'T002_Images'
    __table_args__ = {'schema': 'dsd'} 

    image_id = Column(Integer, primary_key=True, nullable=False)
    document_id = Column(Integer, ForeignKey('dsd.T001_Documents.document_id'), nullable=False)
    url = Column(String, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return '{"image_id":%d, "document_id":%d, "url":"%s", "width":%d, "height":%d, "created_at":"%s"}' % (self.image_id, self.document_id, self.url, self.width, self.height, self.created_at)