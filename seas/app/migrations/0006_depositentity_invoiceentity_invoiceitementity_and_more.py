# Generated by Django 5.1.4 on 2024-12-09 15:06

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_customermatchseatentity_app_customermatchseatentity_state_valid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositEntity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('is_deleted', models.BooleanField(db_index=True, default=False)),
                ('last_update_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('amount', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('payment_code', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('INITIAL', 'Initial'),
                            ('IN_PROGRESS', 'In Progress'),
                            ('SUCCESS', 'Success'),
                            ('FAILED', 'Failed'),
                        ],
                        db_index=True,
                        max_length=11,
                    ),
                ),
                ('tracking_code', models.CharField(db_index=True, max_length=15)),
                (
                    'customer',
                    models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.customerentity'),
                ),
            ],
            options={
                'db_table': 'seas_deposit',
            },
        ),
        migrations.CreateModel(
            name='InvoiceEntity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('is_deleted', models.BooleanField(db_index=True, default=False)),
                ('last_update_time', models.DateTimeField(auto_now=True, db_index=True)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('INITIAL', 'Initial'),
                            ('PENDING', 'Pending'),
                            ('SUCCESS', 'Success'),
                            ('FAILED', 'Failed'),
                        ],
                        db_index=True,
                        max_length=7,
                    ),
                ),
                (
                    'customer',
                    models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.customerentity'),
                ),
                ('deposit', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.depositentity')),
            ],
            options={
                'db_table': 'seas_invoice',
            },
        ),
        migrations.CreateModel(
            name='InvoiceItemEntity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('is_deleted', models.BooleanField(db_index=True, default=False)),
                ('last_update_time', models.DateTimeField(auto_now=True, db_index=True)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('INITIAL', 'Initial'),
                            ('PENDING', 'Pending'),
                            ('SUCCESS', 'Success'),
                            ('FAILED', 'Failed'),
                        ],
                        db_index=True,
                        max_length=7,
                    ),
                ),
                (
                    'customer',
                    models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.customerentity'),
                ),
                (
                    'customer_match_seat',
                    models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.customermatchseatentity'),
                ),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.invoiceentity')),
            ],
            options={
                'db_table': 'seas_invoice_item',
            },
        ),
        migrations.AddConstraint(
            model_name='depositentity',
            constraint=models.CheckConstraint(
                condition=models.Q(('status__in', ['INITIAL', 'IN_PROGRESS', 'SUCCESS', 'FAILED'])),
                name='app_depositentity_status_valid',
            ),
        ),
        migrations.AddConstraint(
            model_name='invoiceentity',
            constraint=models.CheckConstraint(
                condition=models.Q(('status__in', ['INITIAL', 'PENDING', 'SUCCESS', 'FAILED'])),
                name='app_invoiceentity_status_valid',
            ),
        ),
        migrations.AddConstraint(
            model_name='invoiceitementity',
            constraint=models.CheckConstraint(
                condition=models.Q(('status__in', ['INITIAL', 'PENDING', 'SUCCESS', 'FAILED'])),
                name='app_invoiceitementity_status_valid',
            ),
        ),
    ]