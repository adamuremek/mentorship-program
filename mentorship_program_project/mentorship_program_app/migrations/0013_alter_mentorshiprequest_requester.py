# Generated by Django 5.0.1 on 2024-03-14 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0012_alter_mentorshiprequest_requester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorshiprequest',
            name='requester',
            field=models.IntegerField(null=True),
        ),
    ]