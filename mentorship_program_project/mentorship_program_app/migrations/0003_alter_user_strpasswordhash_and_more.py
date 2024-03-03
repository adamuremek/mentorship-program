# Generated by Django 5.0.1 on 2024-02-20 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0002_alter_user_imguserprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='str_password_hash',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='str_password_salt',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='str_role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Mentor', 'Mentor'), ('Mentee', 'Mentee'), ('MentorPending', 'Mentor Pending')], default='', max_length=15),
        ),
    ]
