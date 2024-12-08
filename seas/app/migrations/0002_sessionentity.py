# Generated by Django 5.1.4 on 2024-12-08 12:40

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionEntity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('last_update_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('jti', models.CharField(db_index=True, max_length=120)),
                ('expires_datetime', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('is_revoked', models.BooleanField(db_index=True)),
                (
                    'type',
                    models.CharField(
                        blank=True,
                        choices=[('ACCESS', 'Access'), ('REFRESH', 'Refresh')],
                        db_index=True,
                        max_length=7,
                        null=True,
                    ),
                ),
                (
                    'customer',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name='jwt_tokens',
                        to='app.customerentity',
                    ),
                ),
            ],
            options={
                'db_table': 'seas_session',
                'constraints': [
                    models.CheckConstraint(
                        condition=models.Q(('type__in', ['ACCESS', 'REFRESH'])), name='app_sessionentity_type_valid'
                    )
                ],
            },
        ),
    ]