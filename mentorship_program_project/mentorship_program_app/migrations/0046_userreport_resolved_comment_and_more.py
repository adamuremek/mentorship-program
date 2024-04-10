# Generated by Django 5.0.1 on 2024-04-10 04:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0045_userreport_date_resolved_alter_systemlogs_str_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreport',
            name='resolved_comment',
            field=models.CharField(max_length=3500, null=True),
        ),
        migrations.AlterField(
            model_name='userreport',
            name='date_resolved',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]