# Generated by Django 4.2.7 on 2023-12-19 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_searchresult_alter_medicalkit_expiration_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalkit',
            name='expiration_date1',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='medicalkit',
            name='expiration_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
