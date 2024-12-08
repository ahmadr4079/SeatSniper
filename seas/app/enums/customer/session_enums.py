from django.db import models


class SessionTokenType(models.TextChoices):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"
