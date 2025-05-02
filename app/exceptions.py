from fastapi import HTTPException,status


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class IncorrectLoginException(HTTPException):
    def __init__(self, detail: str = "Incorrect email or password"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers={"WWW-Authenticate": "Bearer"})

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

class EmailExistException(HTTPException):
    def __init__(self, detail: str = "Email already registered"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class TooManyRequestsException(HTTPException):
    def __init__(self, detail: str = "Too many requests"):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail)

class ProductNotFoundException(HTTPException):
    def __init__(self, detail: str = "Product not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class CategoryNotFoundException(HTTPException):
    def __init__(self, detail: str = "Category not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class CartNotFoundException(HTTPException):
    def __init__(self, detail: str = "Cart not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class CartItemNotFoundException(HTTPException):
    def __init__(self, detail: str = "Cart item not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class OrderNotFoundException(HTTPException):
    def __init__(self, detail: str = "Order not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class OrderItemNotFoundException(HTTPException):
    def __init__(self, detail: str = "Order item not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)