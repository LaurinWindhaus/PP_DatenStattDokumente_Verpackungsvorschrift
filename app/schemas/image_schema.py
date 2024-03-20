from pydantic import BaseModel

class ImageReadResponseSchema(BaseModel):
    url: str
    width: int
    height: int

    class Config:
        orm_mode = True

class ImageCreateRequestSchema(ImageReadResponseSchema):
    document_id: int

class ImageUpdateRequestSchema(BaseModel):
    images: list

class ImageDeleteRequestSchema(BaseModel):
    document_id: int
    url: str