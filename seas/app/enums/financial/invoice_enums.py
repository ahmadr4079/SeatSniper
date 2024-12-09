from django.db import models


class InvoiceStatusType(models.TextChoices):
    INITIAL = "INITIAL"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
