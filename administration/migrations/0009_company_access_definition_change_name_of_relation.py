# Generated by Django 2.1.2 on 2018-10-17 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0008_company_access_definition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companyaccess',
            old_name='owner',
            new_name='product',
        ),
    ]
