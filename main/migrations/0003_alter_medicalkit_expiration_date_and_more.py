# Generated by Django 4.2.7 on 2023-12-19 00:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_medicalkit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalkit',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 18, 0, 4, 18, 696828)),
        ),
        migrations.AlterField(
            model_name='medicalkit',
            name='purchase_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]