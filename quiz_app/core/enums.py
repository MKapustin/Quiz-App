import enum
from typing import Any, Optional


class BaseEnum(enum.Enum):
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _, label: Optional[str] = None):
        # ignore the first param since it's already set by __new__
        self._label_ = label or self.value.replace("_", " ").title()

    def __str__(self):
        return self.value

    @property
    def label(self) -> str:
        return self._label_

    @classmethod
    def choices(cls) -> tuple[tuple[Any, str]]:
        return tuple((m.value, m.label) for m in cls)


class QuizState(BaseEnum):
    DRAFT = "Draft"
    ACTIVE = "Active"
    ARCHIVED = "Archived"


class QuizParticipationState(BaseEnum):
    NOT_STARTED = "NOT_STARTED"
    ACTIVE = "ACTIVE"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"


class QuizInvitationState(BaseEnum):
    SENT = "SENT"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
