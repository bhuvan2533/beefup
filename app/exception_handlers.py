from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
import logging
from fastapi.exceptions import HTTPException as FastAPIHTTPException

logger = logging.getLogger(__name__)

class InternalServerError(HTTPException):
    def __init__(self, message: str = "Internal server error occurred."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"statusCode": 500, "message": message}
        )

class InvalidFileTypeException(HTTPException):
    def __init__(self, message: str = "Invalid file type. Supported types are 'jd' and 'profile'."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"statusCode": 400, "message": message}
        )

class ResourceNotFoundException(HTTPException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"statusCode": 404, "message": message}
        )

class BadRequestException(HTTPException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"statusCode": 400, "message": message}
        )

class DatabaseException(HTTPException):
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"statusCode": 500, "message": message}
        )

def http_exception_handler(request: Request, exc: FastAPIHTTPException):
    logger.error(f"HTTPException: {exc.detail}")
    if isinstance(exc.detail, dict) and "statusCode" in exc.detail and "message" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"statusCode": exc.status_code, "message": str(exc.detail)}
    )


def resource_not_found_handler(request: Request, exc: ResourceNotFoundException):
    logger.warning(f"NotFound: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


def invalid_file_type_handler(request: Request, exc: InvalidFileTypeException):
    logger.warning(f"InvalidFileType: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


def internal_server_error_handler(request: Request, exc: InternalServerError):
    logger.error(f"InternalServerError: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled Exception:", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"statusCode": 500, "message": "Internal server error occurred."}
    )

def database_exception_handler(request: Request, exc: DatabaseException):
    logger.error(f"DatabaseException: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content=exc.detail)

def bad_request_handler(request: Request, exc: BadRequestException):
    logger.warning(f"BadRequest: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content=exc.detail)