# Generated by Django 2.1.2 on 2019-01-27 16:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0035_add_robot_notification_add_emails'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='notification',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
