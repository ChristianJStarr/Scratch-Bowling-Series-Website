# Generated by Django 3.1.6 on 2021-12-16 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0019_auto_20211215_1937'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='oil_pattern',
            new_name='oil_pattern_id',
        ),
    ]