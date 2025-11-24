class ConversorException(Exception):
    """Base exception for conoversion-related errors"""

    pass


class StructureException(ConversorException):
    """The data structure does not match the template format."""

    def __init__(
        self,
        message="The data structure does not match the template format.",
        details=None,
    ):
        self.message = message
        self.details = details
        super().__init__(self.message)
