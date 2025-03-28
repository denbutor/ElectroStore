from fastapi import HTTPException,status


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized access"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class NotAuthException(HTTPException):
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class NotFoundUserException(HTTPException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class NotValidCredentialsException(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class TooManyRequestsException(HTTPException):
    def __init__(self, detail: str = "Too many requests"):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail)

class ProductNotFoundException(HTTPException):
    def __init__(self, detail: str = "Product not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)