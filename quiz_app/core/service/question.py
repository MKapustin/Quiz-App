from quiz_app.core import models
from .common import Schema
import quiz_app.core.service.quiz as quiz_service


class QuestionReadDTO(Schema):
    pk: int
    quiz: int
    description: str
    correct_answer_points: int

    @classmethod
    def from_orm(cls, obj: models.Question) -> "QuestionReadDTO":
        return cls(
            pk=obj.pk,
            quiz=obj.quiz_id,
            description=obj.description,
            correct_answer_points=obj.correct_answer_points,
        )


class QuestionRepository:
    def __init__(self, user: models.User):
        self._user = user
        self._quiz_repo = quiz_service.QuizRepository(user=user)

    def list_by_quiz(self, quiz_pk: int) -> list[QuestionReadDTO]:
        quiz_dto = self._quiz_repo.get(pk=quiz_pk)
        questions = models.Question.objects.filter(quiz_id=quiz_dto.pk)
        return [QuestionReadDTO.from_orm(obj) for obj in questions]

    def create(self):
        pass
