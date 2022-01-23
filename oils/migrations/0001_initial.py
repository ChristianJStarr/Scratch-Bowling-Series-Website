# Generated by Django 3.1.6 on 2022-01-14 21:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Oil_Pattern',
            fields=[
                ('pattern_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('pattern_name', models.TextField(default=0)),
                ('pattern_cache', models.BinaryField(blank=True, null=True)),
                ('pattern_db_id', models.IntegerField(default=0)),
                ('pattern_length', models.IntegerField(default=0)),
                ('pattern_volume', models.FloatField(default=0)),
                ('pattern_forward', models.FloatField(default=0)),
                ('pattern_backward', models.FloatField(default=0)),
                ('pattern_ratio', models.TextField(default='')),
            ],
        ),
    ]