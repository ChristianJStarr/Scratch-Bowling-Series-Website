# Generated by Django 3.1.6 on 2021-07-06 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_remove_tournament_sponsor_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='total_games',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]