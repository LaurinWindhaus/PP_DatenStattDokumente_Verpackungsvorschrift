import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.Base import Base

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_document(db_session):
    from app.crud.document_crud import create_document
    result = create_document(db_session, "12345", "SomeInstruction")
    assert result.artikelnummer == "12345"
    assert result.hauptpackvorschrift == "SomeInstruction"
