# Generated by Django 2.1.2 on 2018-10-21 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0023_add_user_role_(user_type)'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_staff',
        ),
    ]
