import django.core.exceptions as django_exceptions
import pydantic
import rest_framework.exceptions as drf_exceptions
from rest_framework import views as drf_views

import quiz_app.core.api.exception_handler as exception_handler


class ApiErrorsMixin:
    """
    Mixin that transforms Django/Python/Pydantic exceptions into rest_framework ones.
    """

    _expected_exceptions = {
        django_exceptions.ValidationError: (
            drf_exceptions.ValidationError,
            exception_handler.get_error_message,
        ),
        PermissionError: (
            drf_exceptions.PermissionDenied,
            exception_handler.get_error_message,
        ),
        pydantic.ValidationError: (
            drf_exceptions.ValidationError,
            exception_handler.get_error_message_from_pydantic,
        ),
    }

    def _transform_exception(self, exc) -> Exception:
        if exception_transformer := self._expected_exceptions.get(type(exc)):
            drf_exception_class, message_extractor = exception_transformer
            return drf_exception_class(message_extractor(exc))

        return exc

    def handle_exception(self, exc):
        exc = self._transform_exception(exc)
        return super().handle_exception(exc)


class BaseApi(ApiErrorsMixin, drf_views.APIView):
    # TODO: Extend view with permission check mixin
    pass
