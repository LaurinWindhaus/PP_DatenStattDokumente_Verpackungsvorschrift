class ImageError(Exception):
    """Base exception class for image errors."""
    pass

class ImageNotFoundError(ImageError):
    """Raised when an image is not found."""
    pass

class DatabaseOperationError(ImageError):
    """Raised for general database operation failures."""
    def __init__(self, original_exception):
        self.original_exception = original_exception