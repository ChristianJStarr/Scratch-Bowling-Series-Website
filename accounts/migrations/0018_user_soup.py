# Generated by Django 3.1.6 on 2021-12-09 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20210925_0446'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='soup',
            field=models.TextField(default=''),
        ),
    ]
