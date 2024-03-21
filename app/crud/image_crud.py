from sqlalchemy.orm import Session
from models.Images import Images
from models.Documents import Documents
from core.image_errors import ImageNotFoundError, DatabaseOperationError
from core.document_errors import DocumentNotFoundError


def get_all_image_url(db: Session, document_id: int) -> list:
    images = db.query(Images).filter(Images.document_id == document_id).order_by(Images.created_at.asc()).all()
    if not images:
        raise ImageNotFoundError(f"No images found for document with ID {document_id}.")
    return images


def upload_image(db: Session, document_id: int, image_url: str, width: int, height: int) -> Images:
    validate_document_id = db.query(Documents).filter(Documents.document_id == document_id).first()
    if validate_document_id is None:
        raise DocumentNotFoundError(f"Document with ID {document_id} not found.")
    new_image = Images(
        document_id=document_id,
        url=image_url,
        width=width,
        height=height
    )
    try:
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
    except Exception as e:
        db.rollback()
        raise DatabaseOperationError(e)
    return new_image


def update_image(db: Session, document_id: int, images: list) -> dict:
    for image in images:
        url = image.get('url')
        width = int(float(image.get('width').replace("px", "")))
        height = int(float(image.get('height').replace("px", "")))

        image_to_update = db.query(Images).filter(Images.document_id == document_id, Images.url == url).first()
        if not image_to_update:
            raise ImageNotFoundError(f"Image with URL {url} not found for document with ID {document_id}.")
        image_to_update.width = width
        image_to_update.height = height
        try:
            db.commit()
            db.refresh(image_to_update)
        except Exception as e:
            db.rollback()
            raise DatabaseOperationError(e)
    return 200


def delete_image(db: Session, document_id: int, image_url: str) -> dict:
    image = db.query(Images).filter(Images.url == image_url, Images.document_id == document_id).first()
    if not image:
        raise ImageNotFoundError(f"Image with URL {image_url} not found for document with ID {document_id}.")
    try:
        db.delete(image)
        db.commit()
        return 200
    except Exception as e:
        db.rollback()
        raise DatabaseOperationError(e)