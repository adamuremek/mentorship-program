# Generated by Django 5.0.1 on 2024-02-23 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0012_alter_mentorshiprequest_mentor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mentorshiprequest',
            name='mentee',
        ),
        migrations.RemoveField(
            model_name='mentorshiprequest',
            name='mentor',
        ),
        migrations.AddField(
            model_name='mentorshiprequest',
            name='mentee',
            field=models.ManyToManyField(related_name='mentee_to_mentor_set', to='mentorship_program_app.user'),
        ),
        migrations.AddField(
            model_name='mentorshiprequest',
            name='mentor',
            field=models.ManyToManyField(related_name='mentor_to_mentee_set', to='mentorship_program_app.user'),
        ),
    ]
