# Generated by Django 3.1.6 on 2021-07-11 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Center',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('center_id', models.CharField(max_length=30)),
                ('center_name', models.TextField()),
                ('center_description', models.TextField()),
                ('location_street', models.TextField()),
                ('location_city', models.TextField()),
                ('location_state', models.TextField()),
                ('location_zip', models.IntegerField()),
            ],
        ),
    ]