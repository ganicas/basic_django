# Generated by Django 2.1.2 on 2018-10-20 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0016_company_access_definition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='device',
        ),
        migrations.AddField(
            model_name='device',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.Company'),
        ),
    ]
