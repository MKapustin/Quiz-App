from .common import BaseApi
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
import django.core.exceptions as core_exceptions
import rest_framework.status as drf_status


import quiz_app.core.service.question as question_service


class QuestionRepositoryMixin:
    @staticmethod
    def get_repository(request: Request) -> question_service.QuestionRepository:
        return question_service.QuestionRepository(request.user)


class QuestionListApi(BaseApi, QuestionRepositoryMixin):
    def get(self, request: Request, quiz_pk: int, **kwargs) -> Response:
        repository = self.get_repository(request)

        try:
            question_dto_list = repository.list_by_quiz(quiz_pk=quiz_pk)
        except core_exceptions.ObjectDoesNotExist as error:
            raise NotFound(error)

        return Response(
            [question_dto.serialize() for question_dto in question_dto_list],
            status=drf_status.HTTP_200_OK,
        )
