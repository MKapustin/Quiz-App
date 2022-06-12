import factory
from quiz_app.core.models import User, Quiz, Question
from django.contrib.auth.hashers import make_password


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    staff = False
    admin = False
    password = factory.LazyFunction(lambda: make_password("pi3.1415"))


class QuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quiz

    author = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence")


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    quiz = factory.SubFactory(QuizFactory)
    description = factory.Faker("sentence")
