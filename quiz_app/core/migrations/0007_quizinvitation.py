# Generated by Django 4.0.5 on 2022-06-11 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [("core", "0006_questionanswer")]

    operations = [
        migrations.CreateModel(
            name="QuizInvitation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("SENT", "Sent"),
                            ("REJECTED", "Rejected"),
                            ("ACCEPTED", "Accepted"),
                        ],
                        default="SENT",
                        max_length=8,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "participant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="invites",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="invites",
                        to="core.question",
                    ),
                ),
            ],
        )
    ]
