# Generated by Django 5.0.1 on 2024-04-10 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0045_alter_notes_cls_created_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='strType',
            field=models.CharField(null=True, max_length=100),
        ),
    ]