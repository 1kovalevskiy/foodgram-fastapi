class CustomException(Exception):
    def __init__(self, message: dict = {"detail": "error"}, code: int = 500):
        self.message = message
        self.code = code


class ValidationException(CustomException):
    def __init__(
            self,
            message: dict = {"detail": "Could not validate data"},
            code: int = 400
    ):
        super().__init__(message=message, code=code)


class CredentialException(CustomException):
    def __init__(
            self,
            message: dict = {"detail": "Учетные данные не были предоставлены."},
            code: int = 401
    ):
        super().__init__(message=message, code=code)


class ForbiddenException(CustomException):
    def __init__(
            self,
            message: dict = {
                "detail": "У вас недостаточно прав для выполнения данного "
                           "действия."
            },
            code: int = 403):
        super().__init__(message=message, code=code)


class NotFoundException(CustomException):
    def __init__(
            self,
            message: dict = {"detail": "Страница не найдена."},
            code: int = 404
    ):
        super().__init__(message=message, code=code)
