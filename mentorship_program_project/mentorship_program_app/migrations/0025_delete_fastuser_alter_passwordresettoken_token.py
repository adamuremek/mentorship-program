# Generated by Django 5.0.1 on 2024-03-20 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship_program_app', '0024_fastuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FastUser',
        ),
        migrations.AlterField(
            model_name='passwordresettoken',
            name='token',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
