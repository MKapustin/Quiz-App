import django
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "quiz_app.settings"
django.setup()

from quiz_app.core.service import question as question_service
import pytest
import quiz_app.core.tests.factories as factories
from quiz_app import core as models


@pytest.mark.django_db
class TestQuestionRepository:
    @pytest.fixture
    def user(self):
        return factories.UserFactory()

    @staticmethod
    def get_repository(user: models.User):
        return question_service.QuestionRepository(user=user)

    def test_get(self, user):
        quiz1 = factories.QuizFactory(author=user)
        questions1 = factories.QuestionFactory.create_batch(size=3, quiz=quiz1)

        quiz2 = factories.QuizFactory(author=user)
        factories.QuestionFactory.build_batch(size=2, quiz=quiz2)

        repository = self.get_repository(user=user)
        question_dto_list = repository.list_by_quiz(quiz_pk=quiz1.pk)

        assert len(question_dto_list) == len(questions1)
        assert sorted(question_dto_list, key=lambda obj: obj.pk) == [
            question_service.QuestionReadDTO(
                pk=question.pk,
                quiz=quiz1.pk,
                description=question.description,
                correct_answer_points=question.correct_answer_points,
            )
            for question in questions1
        ]
