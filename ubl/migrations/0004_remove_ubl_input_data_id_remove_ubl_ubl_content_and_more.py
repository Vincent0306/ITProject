# Generated by Django 5.0.6 on 2024-08-01 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ubl', '0003_alter_ubl_ubl_xml_delete_communicationubl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ubl',
            name='input_data_id',
        ),
        migrations.RemoveField(
            model_name='ubl',
            name='ubl_content',
        ),
        migrations.RemoveField(
            model_name='ubl',
            name='validation_id',
        ),
    ]
