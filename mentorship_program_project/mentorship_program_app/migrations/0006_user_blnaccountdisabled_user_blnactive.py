# Generated by Django 5.0.1 on 2024-02-20 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0005_remove_user_blnaccountdisabled_remove_user_blnactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blnAccountDisabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='blnActive',
            field=models.BooleanField(default=True),
        ),
    ]