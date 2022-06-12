import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = "quiz_app.settings"
django.setup()

import datetime as dt
import unittest.mock as mock

import pytest
import rest_framework.status as drf_status
import rest_framework.test as drf_test

import quiz_app.core.enums as enums
import quiz_app.core.service.quiz as quiz_service
import quiz_app.core.tests.factories as factories
from quiz_app.core.tests.api import common


@pytest.mark.django_db
class TestQuizApi:
    @pytest.fixture
    def user(self):
        return factories.UserFactory()

    @pytest.fixture
    def api_client(self, user) -> drf_test.APIClient:
        api_client = drf_test.APIClient()
        api_client.force_login(user)
        return api_client

    @mock.patch("quiz_app.core.service.quiz.QuizRepository.get")
    def test_get(self, mock_get, user, api_client):
        mock_get.return_value = quiz_service.QuizReadDTO(
            pk=1,
            author=1,
            state=enums.QuizState.DRAFT.value,
            title="Test title",
            created_at=dt.datetime(year=2020, month=12, day=1),
        )

        endpoint = common.build_url("quiz_retrieve", url_kwargs=dict(pk=1))
        response = api_client.get(endpoint)

        mock_get.assert_called_once()
        assert response.status_code == drf_status.HTTP_200_OK
        assert response.json() == {
            "pk": 1,
            "author": 1,
            "created_at": "2020-12-01T00:00:00",
            "state": "Draft",
            "title": "Test title",
        }

    @mock.patch("quiz_app.core.service.quiz.QuizRepository.create")
    def test_create(self, mock_create, user, api_client):
        mock_create.return_value = quiz_service.QuizReadDTO(
            pk=1,
            author=1,
            state=enums.QuizState.DRAFT.value,
            title="Test title",
            created_at=dt.datetime(year=2020, month=12, day=1),
        )

        endpoint = common.build_url("quiz_create")
        data = {
            "title": "Test title"
        }
        response = api_client.post(endpoint, data=data)

        mock_create.assert_called_once_with(create_dto=quiz_service.QuizCreateDTO(title=data["title"]))
        assert response.status_code == drf_status.HTTP_201_CREATED
