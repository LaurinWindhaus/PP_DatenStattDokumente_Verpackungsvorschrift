class DocumentError(Exception):
    """Base exception class for document errors."""
    pass

class DocumentNotFoundError(DocumentError):
    """Raised when a document is not found."""
    pass

class DatabaseOperationError(DocumentError):
    """Raised for general database operation failures."""
    def __init__(self, original_exception):
        self.original_exception = original_exception