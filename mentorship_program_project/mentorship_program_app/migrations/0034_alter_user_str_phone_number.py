# Generated by Django 5.0.1 on 2024-04-08 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0033_alter_notes_cls_created_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='str_phone_number',
            field=models.CharField(max_length=19, null=True),
        ),
    ]