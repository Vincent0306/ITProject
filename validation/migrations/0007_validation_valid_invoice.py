# Generated by Django 5.0.6 on 2024-07-30 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validation', '0006_rename_validated_validation_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='validation',
            name='valid_invoice',
            field=models.FileField(null=True, upload_to='uploadInvoices/'),
        ),
    ]
