# Generated by Django 2.1.2 on 2018-12-01 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0030_add_created_at_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='rescanrobotmachine',
            name='activate_rescan',
            field=models.BooleanField(default=False),
        ),
    ]
