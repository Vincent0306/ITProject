# Generated by Django 5.0.6 on 2024-08-01 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_user_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email_verified',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]
