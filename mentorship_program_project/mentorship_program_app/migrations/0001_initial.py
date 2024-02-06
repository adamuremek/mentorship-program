# Generated by Django 5.0.1 on 2024-02-06 20:22

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clsEmailAddress', models.EmailField(max_length=254, null=True)),
                ('strPasswordHash', models.CharField(max_length=100, null=True)),
                ('strRole', models.CharField(choices=[('Admin', 'Admin'), ('Mentor', 'Mentor'), ('Mentee', 'Mentee')], default='', max_length=10)),
                ('clsDateJoined', models.DateField(default=datetime.date.today)),
                ('clsActiveChangedDate', models.DateField(default=datetime.date.today)),
                ('blnActive', models.BooleanField(default=True)),
                ('blnAccountDisabled', models.BooleanField(default=False)),
                ('strFirstName', models.CharField(max_length=747, null=True)),
                ('strLastName', models.CharField(max_length=747, null=True)),
                ('strPhoneNumber', models.CharField(max_length=15, null=True)),
                ('clsDateofBirth', models.DateField(default=datetime.date.today)),
                ('strGender', models.CharField(default='', max_length=35)),
                ('strPreferredPronouns', models.CharField(max_length=50, null=True)),
                ('strSessionID', models.CharField(default='', max_length=255)),
                ('strSessionKeyHash', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Interests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strInterest', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Organizations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strName', models.CharField(max_length=100)),
                ('strIndustryType', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='System_Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strActivity', models.CharField(max_length=500)),
                ('clsCreatedOn', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Biographies',
            fields=[
                ('intUserID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mentorship_program_app.users')),
                ('strBio', models.CharField(max_length=5000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mentees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intUserID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.users')),
            ],
        ),
        migrations.CreateModel(
            name='Mentors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intMaxMentees', models.IntegerField(default=4)),
                ('intRecommendations', models.IntegerField(default=0)),
                ('strJobTitle', models.CharField(max_length=100)),
                ('intUserID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.users')),
                ('intOrganizationID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.organizations')),
            ],
        ),
        migrations.CreateModel(
            name='Mentor_reports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strReportType', models.CharField(choices=[], default='', max_length=10)),
                ('strReportBody', models.CharField(max_length=3500)),
                ('intMentorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.mentors')),
            ],
        ),
        migrations.CreateModel(
            name='Mentorship_Referrals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intMenteeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.mentees')),
                ('intMentorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.mentors')),
                ('intReferrerUserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.users')),
            ],
        ),
        migrations.CreateModel(
            name='Mentorship_Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intMenteeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.mentees')),
                ('intMentorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.mentors')),
            ],
        ),
        migrations.CreateModel(
            name='Mentorships',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clsStartDate', models.DateField(default=datetime.date.today)),
                ('clsEndDate', models.DateField(null=True)),
                ('intMenteeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.mentees')),
                ('intMentorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.mentors')),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strTitle', models.CharField(max_length=100)),
                ('strBody', models.CharField(max_length=7000)),
                ('clsCreatedOn', models.DateField(default=datetime.date.today)),
                ('intUserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.users')),
            ],
        ),
        migrations.CreateModel(
            name='Organization_Admins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intUserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.users')),
                ('intOrganizationID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.organizations')),
            ],
        ),
        migrations.CreateModel(
            name='User_Interests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intInterestID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.users')),
                ('intUserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.interests')),
            ],
        ),
    ]
