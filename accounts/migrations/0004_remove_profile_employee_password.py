# Generated by Django 5.2.1 on 2025-06-18 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_employee_id_profile_employee_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='employee_password',
        ),
    ]
