# Generated by Django 3.2.15 on 2022-11-10 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demofile', '0002_alter_profile_resume'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('salary', models.PositiveIntegerField()),
            ],
        ),
    ]
