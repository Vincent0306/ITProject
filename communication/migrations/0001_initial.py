# Generated by Django 5.0.6 on 2024-06-22 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('communication_id', models.AutoField(primary_key=True, serialize=False)),
                ('communication_report', models.FileField(upload_to='uploads/communication/')),
            ],
        ),
    ]
