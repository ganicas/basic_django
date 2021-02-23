# Generated by Django 2.1.2 on 2019-02-07 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0036_ame=add_created_and_updated_field_on_notification_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(3, 'operator'), (2, 'supervisor'), (1, 'engineer'), (0, 'admin')], default=0),
        ),
    ]
