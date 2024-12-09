# Generated by Django 5.1.4 on 2024-12-09 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_customermatchseatentity'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='customermatchseatentity',
            name='app_customermatchseatentity_state_valid',
        ),
        migrations.AlterField(
            model_name='customermatchseatentity',
            name='state',
            field=models.CharField(
                choices=[('AVAILABLE', 'Available'), ('RESERVED', 'Reserved'), ('SOLD', 'Sold')],
                db_index=True,
                default='AVAILABLE',
                max_length=9,
            ),
        ),
        migrations.AddConstraint(
            model_name='customermatchseatentity',
            constraint=models.CheckConstraint(
                condition=models.Q(('state__in', ['AVAILABLE', 'RESERVED', 'SOLD'])),
                name='app_customermatchseatentity_state_valid',
            ),
        ),
    ]
