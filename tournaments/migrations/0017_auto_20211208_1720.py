# Generated by Django 3.1.6 on 2021-12-08 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0016_auto_20211204_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='sponsor_image',
            field=models.ImageField(default='sponsor-pictures/default.png', upload_to='sponsor-pictures/'),
        ),
    ]