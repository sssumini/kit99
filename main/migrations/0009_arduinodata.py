# Generated by Django 4.2.7 on 2023-12-19 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_medicalkit_expiration_date1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArduinoData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
