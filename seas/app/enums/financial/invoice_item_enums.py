from django.db import models


class InvoiceItemStatusType(models.TextChoices):
    INITIAL = "INITIAL"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
