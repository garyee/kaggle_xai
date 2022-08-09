class BaseCustomException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return self.msg


class PageDoesNotExistError(BaseCustomException):
    """Raised when the page does not exist"""
