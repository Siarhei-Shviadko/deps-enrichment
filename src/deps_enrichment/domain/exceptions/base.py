__all__ = [
    "EnrichmentException",
    "NotFoundError",
    "IllegalArgument",
    "AlreadyExistsError",
    "ForbiddenError",
    "RestClientError",
    "BusinessException",
]


class EnrichmentException(Exception):
    code = "enrichment_exception"


class BusinessException(EnrichmentException):
    code = "business_exception"


class NotFoundError(EnrichmentException):
    code = "not_found_error"


class IllegalArgument(EnrichmentException):
    code = "illegal_argument"


class AlreadyExistsError(EnrichmentException):
    code = "already_exists_error"


class ForbiddenError(EnrichmentException):
    code = "forbidden_error"


class RestClientError(EnrichmentException):
    code = "rest_client_error"
