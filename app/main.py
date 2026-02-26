from starlette import status
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base
from app.db.session import engine
from app.core.response import error_response
from app.routers import auth_routes, material_routes
from app.core.exceptions import (AppException, NotFoundException, AlreadyExistsException, 
                             UnauthorizedException, PermissionDeniedException, 
                             ExternalServiceException, DatabaseException, 
                             ValidationException, BusinessRuleViolation, 
                             BadRequestException, ConflictException, 
                             ForbiddenException)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/api/auth")
app.include_router(material_routes.router, prefix="/api/material")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Global exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return error_response(str(exc), status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException):
    return error_response(str(exc), status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(AlreadyExistsException)
async def already_exists_handler(request: Request, exc: AlreadyExistsException):
    return error_response(str(exc), status_code=status.HTTP_409_CONFLICT)


@app.exception_handler(UnauthorizedException)
async def unauthorized_handler(request: Request, exc: UnauthorizedException):
    return error_response(str(exc), status_code=status.HTTP_401_UNAUTHORIZED)


@app.exception_handler(PermissionDeniedException)
async def forbidden_handler(request: Request, exc: PermissionDeniedException):
    return error_response(str(exc), status_code=status.HTTP_403_FORBIDDEN)


@app.exception_handler(ValidationException)
async def validation_handler(request: Request, exc: ValidationException):
    return error_response(str(exc), status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(ConflictException)
async def conflict_handler(request: Request, exc: ConflictException):
    return error_response(str(exc), status_code=status.HTTP_409_CONFLICT)


@app.exception_handler(BusinessRuleViolation)
async def business_rule_violation_handler(request: Request, exc: BusinessRuleViolation):
    return error_response(str(exc), status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(DatabaseException)
async def database_exception_handler(request: Request, exc: DatabaseException):
    return error_response(str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.exception_handler(ExternalServiceException)
async def external_service_exception_handler(request: Request, exc: ExternalServiceException):
    return error_response(str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return error_response(str(exc))

@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return error_response(str(exc), status_code=status.HTTP_403_FORBIDDEN)