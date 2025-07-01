class InvalidParameter(Exception):
    """The parameter passed by the client is incorrect."""

class ServiceException(Exception):
    """Capture business logic failure."""

class ExternalServiceException(Exception):
    """Capture integrated component failure."""
