from typing import Optional

import quiz_app.core.enums as quiz_enums
import datetime as dt
from quiz_app.core import models
from .common import Schema


class BaseQuizDTO(Schema):
    title: str


class QuizReadDTO(BaseQuizDTO):
    pk: int
    author: Optional[int]
    state: quiz_enums.QuizState
    created_at: dt.datetime

    @classmethod
    def from_orm(cls, obj: models.Quiz) -> "QuizReadDTO":
        return cls(
            pk=obj.pk,
            author=obj.author_id,
            state=obj.state,
            title=obj.title,
            created_at=obj.created_at,
        )


class QuizCreateDTO(BaseQuizDTO):
    pass


class QuizRepository:
    def __init__(self, user: models.User):
        self._user = user

    def get(self, pk: int) -> QuizReadDTO:
        instance = models.Quiz.objects.get(pk=pk, author=self._user) # TODO: get if either author = user or exists QuizParticipation with participant=user
        return QuizReadDTO.from_orm(instance)

    def list(self):
        pass

    def create(self, create_dto: QuizCreateDTO) -> QuizReadDTO:
        instance = models.Quiz.objects.create(
            author=self._user,
            title=create_dto.title
        )
        return QuizReadDTO.from_orm(instance)
