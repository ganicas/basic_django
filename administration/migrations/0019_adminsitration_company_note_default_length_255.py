# Generated by Django 2.1.2 on 2018-10-20 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0018_adminsitration_company_device_product_on_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='note',
            field=models.TextField(default='', max_length=250),
        ),
    ]
