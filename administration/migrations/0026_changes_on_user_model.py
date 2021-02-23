# Generated by Django 2.1.2 on 2018-10-22 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0025_changes_on_custom_user_role_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(3, 'operator'), (2, 'supervisor'), (1, 'engineer'), (0, 'admin')], default=3),
        ),
    ]