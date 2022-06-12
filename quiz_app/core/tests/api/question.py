import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = "quiz_app.settings"
django.setup()

import unittest.mock as mock

import pytest
import rest_framework.status as drf_status
import rest_framework.test as drf_test

import quiz_app.core.service.question as question_service
import quiz_app.core.tests.factories as factories
from quiz_app.core.tests.api import common


# TODO: move user and api_client fixtures to the conftest (common are)
@pytest.mark.django_db
class TestQuestionApi:
    @pytest.fixture
    def user(self):
        return factories.UserFactory()

    @pytest.fixture
    def api_client(self, user) -> drf_test.APIClient:
        api_client = drf_test.APIClient()
        api_client.force_login(user)
        return api_client

    @mock.patch("quiz_app.core.service.question.QuestionRepository.list_by_quiz")
    def test_list(self, mock_list, user, api_client):
        mock_list.return_value = [
            question_service.QuestionReadDTO(
                pk=1, quiz=1, description="Test description", correct_answer_points=12
            ),
            question_service.QuestionReadDTO(
                pk=2, quiz=1, description="Test description 2", correct_answer_points=3
            ),
        ]

        endpoint = common.build_url("questions_list", url_kwargs=dict(quiz_pk=1))
        response = api_client.get(endpoint)

        mock_list.assert_called_once()
        assert response.status_code == drf_status.HTTP_200_OK
        assert response.json() == [
            {
                "pk": 1,
                "quiz": 1,
                "description": "Test description",
                "correct_answer_points": 12,
            },
            {
                "pk": 2,
                "quiz": 1,
                "description": "Test description 2",
                "correct_answer_points": 3,
            },
        ]
