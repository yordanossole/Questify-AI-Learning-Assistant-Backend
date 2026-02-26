class AppException(Exception):
    pass

class AlreadyExistsException(AppException):
    pass

class NotFoundException(AppException):
    pass

class BadRequestException(AppException):
    pass

class ValidationException(AppException):
    pass

class PermissionDeniedException(AppException):
    pass

class UnauthorizedException(AppException):
    pass

class ConflictException(AppException):
    pass

class BusinessRuleViolation(AppException):
    pass

class DatabaseException(AppException):
    pass

class ExternalServiceException(AppException):
    pass

class InvalidCredentials(AppException):
    pass

class ForbiddenException(AppException):
    pass