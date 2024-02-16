class UtilException(Exception):
    """There was an ambiguous exception."""


class UtilRuntimeError(UtilException):
    """Runtime error."""


class UtilTypeError(UtilException):
    """Type error."""
