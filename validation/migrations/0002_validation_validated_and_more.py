# Generated by Django 5.0.6 on 2024-07-24 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='validation',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='validation',
            name='validation_report',
            field=models.FileField(null=True, upload_to='uploads/validation/'),
        ),
    ]
