# Generated by Django 3.2.15 on 2022-10-21 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bus', '0008_alter_reservation_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='buslist',
            name='available_seats',
            field=models.PositiveIntegerField(default=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buslist',
            name='total_seats',
            field=models.PositiveIntegerField(default=75),
            preserve_default=False,
        ),
    ]
