# Generated by Django 2.1.1 on 2018-10-10 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_add_device_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.CharField(default='', max_length=45)),
                ('active', models.BooleanField(default=False)),
                ('connection_status', models.SmallIntegerField(default=0)),
                ('tolerated_offline', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('device_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.DeviceType')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.Company')),
            ],
        ),
    ]