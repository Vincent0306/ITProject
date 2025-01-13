# Generated by Django 5.0.6 on 2024-06-22 11:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inputdata', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputdata',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AddField(
            model_name='communicationinputdata',
            name='input_data_id',
            field=models.ForeignKey(db_column='input_data_id', on_delete=django.db.models.deletion.CASCADE, to='inputdata.inputdata'),
        ),
    ]
