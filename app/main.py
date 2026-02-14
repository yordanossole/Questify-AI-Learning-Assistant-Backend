from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from core.exceptions import *
from core.response import error_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(exc: AppException):
    return error_response(str(exc), status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(NotFoundException)
async def not_found_handler(exc: NotFoundException):
    return error_response(str(exc), status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(AlreadyExistsException)
async def already_exists_handler(exc: AlreadyExistsException):
    return error_response(str(exc), status_code=status.HTTP_409_CONFLICT)


@app.exception_handler(UnauthorizedException)
async def unauthorized_handler(exc: UnauthorizedException):
    return error_response(str(exc), status_code=status.HTTP_401_UNAUTHORIZED)


@app.exception_handler(PermissionDeniedException)
async def forbidden_handler(exc: PermissionDeniedException):
    return error_response(str(exc), status_code=status.HTTP_403_FORBIDDEN)


@app.exception_handler(ValidationException)
async def validation_handler(exc: ValidationException):
    return error_response(str(exc), status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(ConflictException)
async def conflict_handler(exc: ConflictException):
    return error_response(str(exc), status_code=status.HTTP_409_CONFLICT)


@app.exception_handler(BusinessRuleViolation)
async def business_rule_violation_handler(exc: BusinessRuleViolation):
    return error_response(str(exc), status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(DatabaseException)
async def database_exception_handler(exc: DatabaseException):
    return error_response(str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.exception_handler(ExternalServiceException)
async def external_service_exception_handler(exc: ExternalServiceException):
    return error_response(str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
