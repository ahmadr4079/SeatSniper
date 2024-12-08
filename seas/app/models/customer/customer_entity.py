from django.db import models

from seas.app.models.base_entity import EditableEntity


class CustomerEntity(EditableEntity):
    username = models.CharField(max_length=80, null=True, blank=True)
    name = models.CharField(max_length=80, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True, db_index=True, unique=True)
    last_login_time = models.DateTimeField(null=True, blank=True)

    @property
    def is_authenticated(self):
        return True

    class Meta:
        db_table = 'seas_customer'
        app_label = 'app'
