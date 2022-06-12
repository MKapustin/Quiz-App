from django.urls import path

from quiz_app.core.api.quiz import QuizRetrieveApi, QuizCreateApi
from quiz_app.core.api.question import QuestionListApi


urlpatterns = [
    path("api/quiz/", QuizCreateApi.as_view(), name="quiz_create"),
    path("api/quiz/<int:pk>/", QuizRetrieveApi.as_view(), name="quiz_retrieve"),
    path(
        "api/quiz/<int:quiz_pk>/questions/",
        QuestionListApi.as_view(),
        name="questions_list",
    ),
]
