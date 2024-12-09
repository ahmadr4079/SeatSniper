from django.db import models


class DepositStatusType(models.TextChoices):
    INITIAL = "INITIAL"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
