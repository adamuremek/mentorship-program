# Generated by Django 5.0.1 on 2024-03-15 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0016_rename_request_mentorshiprequest_requester'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mentor',
            old_name='organizations',
            new_name='organization',
        ),
    ]
