# Generated by Django 2.1.2 on 2018-12-31 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robots_machine', '0009_extend_robot_working_progress_ideal_cycle_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='robotworkingprogress',
            name='total_count',
            field=models.IntegerField(default=0),
        ),
    ]
