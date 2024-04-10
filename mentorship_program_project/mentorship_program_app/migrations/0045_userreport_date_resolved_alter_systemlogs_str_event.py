# Generated by Django 5.0.1 on 2024-04-10 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0044_alter_user_str_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreport',
            name='date_resolved',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='systemlogs',
            name='str_event',
            field=models.CharField(choices=[('User logged on', 'Logon Event'), ('Create mentorship', 'Approve Mentorship Event'), ('Request mentorship', 'Request Mentorship Event'), ('Mentorship terminated', 'Mentorship Terminated Event'), ('Mentee signed up', 'Mentee Register Event'), ('Mentor applied', 'Mentor Register Event'), ('Mentee deactivated', 'Mentee Deactivated Event'), ('Mentor deactivated', 'Mentor Deactivated Event'), ('Interest created', 'Interests Created Event'), ('Interest updated', 'Interests Updated Event'), ('Interest deleted', 'Interests Deleted Event'), ('Mentor approved', 'Mentor Approved Event'), ('Mentor denied', 'Mentor Denied Event'), ('Report resolved', 'Report Resolved Event'), ('Report created', 'Report Created Event'), ('Mentee inactivated', 'Mentee Inactivated Event'), ('Mentor inactivated', 'Mentor Inactivated Event'), ('Organization deleted', 'Organization Deleted Event'), ('Organization added', 'Organization Created Event'), ("Mentor's organization changed", 'Mentor Organization Changed Event')], default='', max_length=500),
        ),
    ]