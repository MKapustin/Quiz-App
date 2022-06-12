import pydantic
from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import Response, exception_handler


def _get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def get_error_message(exc):
    if hasattr(exc, "message_dict"):
        return exc.message_dict
    error_msg = _get_first_matching_attr(exc, "message", "messages", "detail")

    if isinstance(error_msg, list):
        error_msg = ", ".join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg


def get_error_message_from_pydantic(exc: pydantic.ValidationError) -> dict:
    return {error["loc"][0]: [error["msg"]] for error in exc.errors()}


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    # if there is an IntegrityError and the error response hasn't already been generated
    if isinstance(exc, IntegrityError) and not response:
        response = Response(
            {
                "message": "It seems there is a conflict between the data you are trying to save and your current "
                "data. Please review your entries and try again."
            },
            status=status.HTTP_409_CONFLICT,
        )

    return response
