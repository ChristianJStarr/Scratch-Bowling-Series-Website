# Generated by Django 3.1.6 on 2022-01-08 22:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Drawer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('opened_datetime', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('closed_datetime', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('amount', models.IntegerField(default=0)),
                ('opened', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='drawers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('datetime', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('amount', models.IntegerField(default=0)),
                ('drawer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='prolink.drawer')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]