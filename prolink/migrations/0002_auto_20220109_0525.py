# Generated by Django 3.1.6 on 2022-01-09 10:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('prolink', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
