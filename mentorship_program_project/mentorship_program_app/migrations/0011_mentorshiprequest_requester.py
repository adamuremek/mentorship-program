# Generated by Django 5.0.1 on 2024-03-14 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0010_rename_img_profile_profileimg_img_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentorshiprequest',
            name='requester',
            field=models.TextField(max_length=100, null=True),
        ),
    ]