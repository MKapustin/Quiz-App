import django
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "quiz_app.settings"
django.setup()

from quiz_app.core.service import quiz as quiz_service
import pytest
import quiz_app.core.tests.factories as factories
from quiz_app import core as models
from quiz_app.core import enums


@pytest.mark.django_db
class TestQuizRepository:
    @pytest.fixture
    def user(self):
        return factories.UserFactory()

    @staticmethod
    def get_repository(user: models.User):
        return quiz_service.QuizRepository(user=user)

    def test_get(self, user):
        quiz = factories.QuizFactory(author=user)
        repository = self.get_repository(user=user)

        quiz_dto = repository.get(pk=quiz.pk)

        assert quiz_dto == quiz_service.QuizReadDTO(
            pk=quiz.pk,
            author=user.pk,
            state=quiz.state,
            title=quiz.title,
            created_at=quiz.created_at,
        )

    def test_create(self, user):
        repository = self.get_repository(user=user)

        create_dto = quiz_service.QuizCreateDTO(title="Test title")
        quiz_dto = repository.create(create_dto=create_dto)

        assert quiz_dto.title == create_dto.title
        assert quiz_dto.author == user.pk
        assert quiz_dto.state == enums.QuizState.DRAFT
