from sqlalchemy.orm import Session
from models.Documents import Documents
from core.document_errors import DocumentNotFoundError, DatabaseOperationError


def get_document(db: Session, document_id: int):
    document = db.query(Documents).filter(Documents.document_id == document_id).first()
    if not document:
        raise DocumentNotFoundError(f"Document with ID {document_id} not found.")
    return document


def create_document(db: Session, artikelnummer: str, hauptpackvorschrift: str):
    new_document = Documents (
        artikelnummer=artikelnummer,
        hauptpackvorschrift=hauptpackvorschrift,
        data={}
    )
    try:
        db.add(new_document)
        db.commit()
        db.refresh(new_document)
    except Exception as e:
        db.rollback()
        raise DatabaseOperationError(e)
    return new_document


def get_documents(db: Session, artikelnummer: str = None):
    query = db.query(Documents)
    if artikelnummer:
        query = query.filter(Documents.artikelnummer.like(f"%{artikelnummer}%"))
    result = query.all()
    return result


def update_document(db: Session, document_id: int, new_data: dict):
    document_to_update = db.query(Documents).filter(Documents.document_id == document_id).first()
    if not document_to_update:
        raise DocumentNotFoundError(f"Document with ID {document_id} not found.")
    try:
        document_to_update.data = new_data
        db.commit()
        return document_to_update
    except Exception as e:
        db.rollback()
        raise DatabaseOperationError(e)


def delete_document(db: Session, document_id: int):
    document_to_delete = db.query(Documents).filter(Documents.document_id == document_id).first()
    if not document_to_delete:
        raise DocumentNotFoundError(f"Document with ID {document_id} not found.")
    try:
        db.delete(document_to_delete)
        db.commit()
        return 200
    except Exception as e:
        db.rollback()
        raise DatabaseOperationError(e)