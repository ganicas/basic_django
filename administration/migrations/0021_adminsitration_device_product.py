# Generated by Django 2.1.2 on 2018-10-20 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0020_adminsitration_company_name_device_name_and_product_name_unique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='administration.Product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='administration.Company'),
        ),
    ]