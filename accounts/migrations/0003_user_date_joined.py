# Generated by Django 3.1.6 on 2021-07-03 05:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210703_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateField(default=datetime.date.today, editable=False),
        ),
    ]
