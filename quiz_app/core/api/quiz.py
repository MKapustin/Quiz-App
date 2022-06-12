from .common import BaseApi
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
import django.core.exceptions as core_exceptions
import rest_framework.status as drf_status


import quiz_app.core.service.quiz as quiz_service


class QuizRepositoryMixin:
    @staticmethod
    def get_repository(request: Request) -> quiz_service.QuizRepository:
        return quiz_service.QuizRepository(request.user)


class QuizRetrieveApi(BaseApi, QuizRepositoryMixin):
    def get(self, request: Request, pk: int, **kwargs) -> Response:
        repository = self.get_repository(request)

        try:
            quiz_dto = repository.get(pk)
        except core_exceptions.ObjectDoesNotExist as error:
            raise NotFound(error)

        return Response(quiz_dto.serialize(), status=drf_status.HTTP_200_OK)


class QuizCreateApi(BaseApi, QuizRepositoryMixin):
    def post(self, request: Request, **kwargs) -> Response:
        repository = self.get_repository(request)
        create_dto = quiz_service.QuizCreateDTO(**request.data)

        try:
            quiz_dto = repository.create(create_dto=create_dto)
        except core_exceptions.ObjectDoesNotExist as error:
            raise NotFound(error)

        return Response(quiz_dto.serialize(), status=drf_status.HTTP_201_CREATED)
