# Generated by Django 3.1.6 on 2021-07-03 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_date_joined'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='hand',
        ),
        migrations.AddField(
            model_name='user',
            name='left_handed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='right_handed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='location_city',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='location_state',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='location_street',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(null=True, upload_to='profile-pictures/'),
        ),
    ]