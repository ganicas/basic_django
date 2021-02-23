# Generated by Django 2.1.2 on 2018-12-01 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0028_add_robot_machine_rescan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Robots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('serial_number', models.CharField(default='', max_length=100)),
                ('note', models.TextField(default='', max_length=250)),
                ('enabled', models.BooleanField(default=True)),
                ('city', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=100)),
                ('address', models.CharField(default='', max_length=200)),
                ('active', models.BooleanField(default=False)),
                ('robot_ip_address', models.GenericIPAddressField(protocol='IPv4')),
                ('robot_username', models.CharField(max_length=255)),
                ('robot_password', models.CharField(max_length=255)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='administration.Company')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='administration.Product')),
            ],
            options={
                'db_table': 'robots_machine',
            },
        ),
    ]