# Generated by Django 3.1.6 on 2021-07-03 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210703_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='assets/profile-pictures/default.jpg', upload_to='assets/profile-pictures/'),
        ),
    ]