# Generated by Django 5.0.1 on 2024-02-26 17:32

import datetime
import django.db.models.deletion
import mentorship_program_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cls_email_address', models.EmailField(max_length=254, null=True, unique=True)),
                ('str_password_hash', models.CharField(max_length=1000, null=True)),
                ('str_password_salt', models.CharField(max_length=1000, null=True)),
                ('str_role', models.CharField(choices=[('Admin', 'Admin'), ('Mentor', 'Mentor'), ('Mentee', 'Mentee'), ('MentorPending', 'Mentor Pending'), ('Graduated', 'Graduated'), ('Declined', 'Declined')], default='', max_length=15)),
                ('cls_date_joined', models.DateField(default=datetime.date.today)),
                ('cls_active_changed_date', models.DateField(default=datetime.date.today)),
                ('bln_active', models.BooleanField(default=True)),
                ('bln_account_disabled', models.BooleanField(default=False)),
                ('str_first_name', models.CharField(max_length=747, null=True)),
                ('str_last_name', models.CharField(max_length=747, null=True)),
                ('str_phone_number', models.CharField(max_length=15, null=True)),
                ('cls_date_of_birth', models.DateField(default=datetime.date.today)),
                ('str_gender', models.CharField(default='', max_length=35)),
                ('str_preferred_pronouns', models.CharField(max_length=50, null=True)),
                ('img_user_profile', models.ImageField(default='images/default_profile_picture.png', upload_to='images/')),
            ],
            bases=(mentorship_program_app.models.SVSUModelData, models.Model),
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strInterest', models.CharField(max_length=100, unique=True)),
                ('isDefaultInterest', models.BooleanField(default=False)),
            ],
            bases=(mentorship_program_app.models.SVSUModelData, models.Model),
        ),
        migrations.CreateModel(
            name='SystemLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strActivity', models.CharField(max_length=500)),
                ('clsCreatedOn', models.DateField(default=datetime.date.today)),
            ],
            bases=(mentorship_program_app.models.SVSUModelData, models.Model),
        ),
        migrations.CreateModel(
            name='Biographies',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mentorship_program_app.user')),
                ('strBio', models.CharField(max_length=5000, null=True)),
            ],
            bases=(mentorship_program_app.models.SVSUModelData, models.Model),
        ),
        migrations.AddField(
            model_name='user',
            name='interests',
            field=models.ManyToManyField(to='mentorship_program_app.interest'),
        ),
        migrations.CreateModel(
            name='Mentee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.user')),
            ],
            bases=(mentorship_program_app.models.SVSUModelData, models.Model),
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intMaxMentees', models.IntegerField(default=4)),
                ('intRecommendations', models.IntegerField(default=0)),
                ('strJobTitle', models.CharField(max_length=100)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.user')),
            ],
            bases=(mentorship_program_app.models.SVSUModelData, models.Model),
        ),
        migrations.CreateModel(
            name='MentorReports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strReportType', models.CharField(choices=[], default='', max_length=10)),
                ('strReportBody', models.CharField(max_length=3500)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.mentor')),
            ],
            bases=(mentorship_program_app.models.SVSUModelData, models.Model),
        ),
        migrations.CreateModel(
            name='MentorshipReferral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.mentee')),
                ('mentor_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_referrals_set', to='mentorship_program_app.mentor')),
                ('mentor_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referral_set', to='mentorship_program_app.mentor')),
            ],
            bases=(mentorship_program_app.models.SVSUModelData, models.Model),
        ),
        migrations.CreateModel(
            name='MentorshipRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentee_to_mentor_set', to='mentorship_program_app.user')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentor_to_mentee_set', to='mentorship_program_app.user')),
            ],
            bases=(mentorship_program_app.models.SVSUModelData, models.Model),
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strTitle', models.CharField(max_length=100)),
                ('strBody', models.CharField(max_length=7000)),
                ('clsCreatedOn', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship_program_app.user')),
            ],
            bases=(mentorship_program_app.models.SVSUModelData, models.Model),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strName', models.CharField(max_length=100)),
                ('strIndustryType', models.CharField(max_length=100)),
                ('admins', models.ManyToManyField(to='mentorship_program_app.mentor')),
            ],
            bases=(mentorship_program_app.models.SVSUModelData, models.Model),
        ),
    ]
