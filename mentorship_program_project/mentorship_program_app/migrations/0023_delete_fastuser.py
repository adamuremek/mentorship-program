# Generated by Django 5.0.1 on 2024-03-18 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0022_fastuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FastUser',
        ),
    ]