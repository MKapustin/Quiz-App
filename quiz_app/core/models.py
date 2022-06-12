import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

import quiz_app.core.enums as quiz_enums


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff_user(self, email, password):
        user = self.create_user(email, password=password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.staff = True
        user.admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email & Password are required by default

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    objects = UserManager()


class Quiz(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="quizzes"
    )
    # Instead of deleting quiz, it should be marked as Archived in most cases (soft delete)
    state = models.CharField(
        max_length=8,
        choices=quiz_enums.QuizState.choices(),
        default=quiz_enums.QuizState.DRAFT.value,
    )
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    description = models.TextField()
    correct_answer_points = models.IntegerField(default=10)


class QuestionOption(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    description = models.TextField()
    is_correct = models.BooleanField(default=False)


class QuizParticipation(models.Model):
    quiz = models.ForeignKey(
        Question, on_delete=models.PROTECT, related_name="participations"
    )
    participant = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="participations"
    )
    state = models.CharField(
        max_length=11,
        choices=quiz_enums.QuizParticipationState.choices(),
        default=quiz_enums.QuizParticipationState.NOT_STARTED.value,
    )


class QuestionAnswer(models.Model):
    class Meta:
        unique_together = ("participation", "question", "chosen_question_option")

    participation = models.ForeignKey(
        QuizParticipation, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    chosen_question_option = models.ForeignKey(
        QuestionOption, on_delete=models.CASCADE, related_name="answers"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class QuizInvitation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, null=False, unique=True, editable=False)
    quiz = models.ForeignKey(Question, on_delete=models.PROTECT, related_name="invites")
    participant = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="invites"
    )
    state = models.CharField(
        max_length=8,
        choices=quiz_enums.QuizInvitationState.choices(),
        default=quiz_enums.QuizInvitationState.SENT.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
