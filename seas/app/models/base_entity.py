import uuid

from django.db import models


class BaseEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creation_time = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        indexes = [models.Index(fields=["creation_time"])]


class DeletableEntity(BaseEntity):
    is_deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True
        indexes = [models.Index(fields=["is_deleted"])]


class EditableEntity(BaseEntity):
    last_update_time = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
        indexes = [models.Index(fields=["last_update_time"])]
