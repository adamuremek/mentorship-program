# Generated by Django 5.0.1 on 2024-03-18 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0021_passwordresettoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentorreports',
            name='bln_resolved',
            field=models.BooleanField(default=False),
        ),
    ]
