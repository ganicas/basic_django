from django.db import models
from administration.models import AdminSetter
from django.utils import timezone


class Robots(AdminSetter, models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    serial_number = models.CharField(max_length=100, default="")
    note = models.TextField(max_length=250, default="")
    enabled = models.BooleanField(default=True)
    city = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=200, default="")
    company = models.ForeignKey("administration.Company", on_delete=models.DO_NOTHING, null=True)
    product = models.ForeignKey('administration.Product', on_delete=models.DO_NOTHING, blank=True, null=True,)
    active = models.BooleanField(default=False)
    robot_ip_address = models.GenericIPAddressField(protocol='IPv4', blank=False, null=False)
    robot_username = models.CharField(max_length=255, blank=False, null=False)
    robot_password = models.CharField(max_length=255, blank=False, null=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    planned_production_min = models.IntegerField(default=420)
    ideal_cycle_second = models.IntegerField(default=60)

    class Meta:
        db_table = 'robots_machine'


class RobotWorkingProgress(models.Model):
    robot_datetime = models.DateTimeField()
    robot = models.ForeignKey("Robots", on_delete=models.DO_NOTHING, null=True)
    updated = models.DateTimeField(default=timezone.now)

    # OEE info
    active_alarms = models.IntegerField(default=0)
    rejected_units = models.IntegerField(default=0)
    produced_units = models.IntegerField(default=0)
    excepted_units = models.IntegerField(default=0)

    # from robot micro service
    good_units = models.IntegerField(default=0)
    intensity_max = models.IntegerField(default=0)
    errors = models.IntegerField(default=0)
    max_errors = models.IntegerField(default=0)
    big_errors_type1 = models.IntegerField(default=0)
    big_errors_type2 = models.IntegerField(default=0)
    errors_max_type1 = models.IntegerField(default=0)
    errors_max_type2 = models.IntegerField(default=0)
    intensity = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
    good_intensity = models.IntegerField(default=0)

    class Meta:
        db_table = 'robot_working_progress'

