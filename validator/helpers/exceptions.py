
import sys
import traceback

def exception_as_string(err):
    """
    A helper function that converts an exception and is stack trace to something that
    can be viewed and passed around as a string.

    :param: an exception
    :return: string
    """
    trace = traceback.print_exc(file=sys.stdout)

    return str(err) +" | "+ str(trace)


class ReferenceError(Exception):
    """ Raised when a provided reference source is invalid
    """

    def __init__(self, message):
        self.message = message


class BadReferalError(Exception):
    """ Raised when the information provide is insufficiant to identify a key piece of reference data"""

    def __init__(self, message):
        self.message = message


class ConfigurationError(Exception):
    """ Raised due to an incompatible or incomplete configuration"""

    def __init__(self, message):
        self.message = message


class MappingError(Exception):
    """ Raised because a duplicate or incomplete function is being mapped"""

    def __init__(self, message):
        self.message = message