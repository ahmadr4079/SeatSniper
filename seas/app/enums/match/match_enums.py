from django.db import models


class MatchStateType(models.TextChoices):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class CustomerMatchSeatStateType(models.TextChoices):
    RESERVED = "RESERVED"
    SOLD = "SOLD"
    CANCELED = "CANCELED"
