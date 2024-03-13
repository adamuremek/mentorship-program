# Generated by Django 5.0.1 on 2024-03-13 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0009_alter_systemlogs_str_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemlogs',
            name='str_event',
            field=models.CharField(choices=[('Logon', 'Logon Event'), ('Create Mentorship', 'Approve Mentorship Event'), ('Request Mentorship', 'Request Mentorship Event'), ('Mentee signed up', 'Mentee Register Event'), ('Mentor applied', 'Mentor Register Event'), ('Mentee deactivated', 'Mentee Deactivated'), ('Mentor deactivated', 'Mentor Deactivated')], default='', max_length=500),
        ),
    ]
