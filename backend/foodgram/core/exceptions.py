from fastapi import HTTPException, status


def validations_exception(message: str | None = None):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message or "Could not validate data",
    )


def credentials_exception(message: str | None = None):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message or "Учетные данные не были предоставлены.",
    )


def forbidden_exception(message: str | None = None):
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=message or "У вас недостаточно прав для выполнения данного "
                          "действия.",
    )


def not_found_exception(message: str | None = None):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=message or "Страница не найдена.",
    )
