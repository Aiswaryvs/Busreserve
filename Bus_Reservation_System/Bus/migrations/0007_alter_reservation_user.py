# Generated by Django 3.2.15 on 2022-10-19 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bus', '0006_alter_buslist_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
