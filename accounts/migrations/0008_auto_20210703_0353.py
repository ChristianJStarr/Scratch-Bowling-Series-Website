# Generated by Django 3.1.6 on 2021-07-03 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210703_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='location_zip',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]