# Generated by Django 5.0.1 on 2024-04-09 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0037_alter_systemlogs_cls_log_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemlogs',
            name='cls_log_created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
