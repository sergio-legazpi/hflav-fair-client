class SourceException(Exception):
    """Base exception for source-related errors"""

    pass


class DataAccessException(SourceException):
    """Error accessing data source"""

    def __init__(self, message="Error accessing data source", details=None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class DataNotFoundException(SourceException):
    """Error when data is not found"""

    def __init__(self, message="No data found", details=None):
        self.message = message
        self.details = details
        super().__init__(self.message)
