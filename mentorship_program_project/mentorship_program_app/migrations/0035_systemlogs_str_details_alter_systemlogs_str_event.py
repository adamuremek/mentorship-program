# Generated by Django 5.0.1 on 2024-04-09 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0034_alter_user_str_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemlogs',
            name='str_details',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='systemlogs',
            name='str_event',
            field=models.CharField(choices=[('User logged on', 'Logon Event'), ('Create mentorship', 'Approve Mentorship Event'), ('Request mentorship', 'Request Mentorship Event'), ('Mentorship terminated', 'Mentorship Terminated Event'), ('Mentee signed up', 'Mentee Register Event'), ('Mentor applied', 'Mentor Register Event'), ('Mentee deactivated', 'Mentee Deactivated Event'), ('Mentor deactivated', 'Mentor Deactivated Event'), ('Interest created', 'Interests Created'), ('Interest updated', 'Interests Updated'), ('Interest deleted', 'Interests Deleted')], default='', max_length=500),
        ),
    ]
