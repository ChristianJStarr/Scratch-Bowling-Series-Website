# Generated by Django 3.1.6 on 2022-01-10 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentdata',
            name='is_winner',
            field=models.BooleanField(default=False),
        ),
    ]
