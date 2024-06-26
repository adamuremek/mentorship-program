# Generated by Django 5.0.1 on 2024-04-10 00:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0044_merge_20240409_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='cls_created_on',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='systemlogs',
            name='cls_log_created_on',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='cls_active_changed_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='cls_date_joined',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='str_last_login_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
