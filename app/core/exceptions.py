class AppException(Exception):
    pass

class AlreadyExistsException(Exception):
    pass

class NotFoundException(Exception):
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
