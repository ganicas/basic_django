# Generated by Django 2.1.2 on 2018-12-03 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robots_machine', '0003_add_robot_working_progres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='robotworkingprogress',
            name='message',
        ),
        migrations.RemoveField(
            model_name='robotworkingprogress',
            name='working_status',
        ),
    ]
