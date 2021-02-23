# Generated by Django 2.1.2 on 2018-10-20 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0015_extend_product_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyaccess',
            name='product',
        ),
        migrations.AddField(
            model_name='companyaccess',
            name='device_tracking',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='companyaccess',
            name='product_tracking',
            field=models.BooleanField(default=False),
        ),
    ]
