from pydantic import BaseModel


class DocumentEditRequestSchema(BaseModel):
    document_id: int

class DocumentCreateRequestSchema(BaseModel):
    artikelnummer: str
    hauptpackvorschrift: str

class DocumentCreateResponseSchema(BaseModel):
    document_id: int
    artikelnummer: str
    hauptpackvorschrift: str

    class Config:
        orm_mode = True

class DocumentUpdateRequestSchema(BaseModel):
    data: dict

class DocumentUpdateResponseSchemaWithData(DocumentCreateResponseSchema):
    data: dict