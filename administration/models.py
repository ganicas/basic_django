from datetime import timezone, datetime
from enum import Enum

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.validators import RegexValidator
from pexpect.replwrap import basestring
from pytz import timezone as pytz_timezone
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone

# Create your models here.
from administration.mixin import UserRolePermissions

USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'
"""
class CustomUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    #user = models.OneToOneField(settings.AUTH_USER_MODEL)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="users/", blank=True, null=True)
    avatar_thumb = models.ImageField(upload_to="users/thumb/", blank=True, null=True)
    timezone = models.CharField(max_length=50, default="Europe/Zagreb")
    role = models.SmallIntegerField(default=0)
    company = models.ForeignKey("Company", blank=True, null=True, on_delete=models.SET_NULL)
    preferred_language = models.CharField(max_length=2, default="en")
    notify_email = models.BooleanField(default=False)
    notify_sms = models.BooleanField(default=False)
    assigned_companies = models.ManyToManyField('Company', blank=True, related_name="company_assignments")
    access_all_company = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['user']
    USERNAME_FIELD = 'user'

    def __str__(self):
        return str(self.user.username)

    def __unicode__(self):
        return str(self.user.username)

    class Meta:
        db_table = 'custom_users'


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            CustomUser.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)
"""


class AdminSetter(models.Model):

    class Meta:
        abstract = True

    def set_string(self, attr, value):
        from django.db.models.fields import CharField as CharField
        value = value.strip()

        # if field is CharField, limit the length
        model_attr = self._meta.get_field(attr)
        if isinstance(model_attr, CharField):
            value = value[:model_attr.max_length]

        setattr(self, attr, value)

    def set_int(self, attr, value, default=0):
        try:
            value = str(value)
            value = value.split(".")[0]
            value = value.split(",")[0]
            value = int(value)
        except ValueError:
            value = default
        setattr(self, attr, value)

    def set_bool(self, attr, value):
        new_value = value != "" if isinstance(value, basestring) else value
        modified = new_value != getattr(self, attr)
        setattr(self, attr, new_value)
        return modified

    def set_url(self, attr, value):
        value = value.strip()
        if len(value) != 0 and not value.startswith(("http://", "https://",)):
            value = "http://" + value
        setattr(self, attr, value)

    def set_date(self, attr, value):
        import datetime
        try:
            dd, mm, yy = value.split(".")
            value = datetime.date(int(yy), int(mm), int(dd))
        except Exception as e:
            value = None

        setattr(self, attr, value)

    def set_datetime(self, attr, value):
        import datetime
        try:
            value = timezone.make_aware(datetime.strptime(value,"%d.%m.%Y %H:%M"), timezone.get_current_timezone())
        except:
            value = None

        setattr(self, attr, value)

    def set_time(self, attr, value):
        import datetime
        try:
            value = datetime.datetime.strptime(value, "%H:%M:%S")
        except:
            try:
                value = datetime.datetime.strptime(value, "%H:%M")
            except:
                value = None
        setattr(self, attr, value)

    def set_foreign_object(self, attr, obj_class, id, check_object_modified=False):
        try:
            value = obj_class.all_objects.get(id=id)
        except:
            value = None

        modified = check_object_modified and getattr(self, attr) != value
        setattr(self, attr, value)
        return modified

    def split_string(self, attr, max_count=5, separator='|'):
        value = getattr(self, attr)
        return ([s for s in value.split(separator) if len(s) > 0] + [""] * max_count)[:max_count]

    def join_string(self, attr, value, separator='|'):
        value = separator.join([s.strip() for s in value if len(s.strip()) > 0])
        setattr(self, attr, value)

    def get_media_repository_hash(self):
        import hashlib
        return hashlib.sha1("%s %d" % (self.__class__.__name__, self.id)).hexdigest() if self.id else ""

    def get_media_repository_path(self):
        import os
        return os.path.realpath("%sarticle_images/%s" % (settings.DATA_ROOT, self.get_media_repository_hash())) + "/" if self.id else ""

    def get_media_repository_url(self):
        return "%s/article_images/%s/" % (settings.DATA_URL, self.get_media_repository_hash()) if self.id else ""

    @classmethod
    def create_object(cls, id):
        try:
            id = int(id)
        except ValueError:
            id = 0

        new_item = id == 0
        item = None

        if not new_item:
            try:
                item = cls.objects.get(id=id)
            except:
                new_item = True

        if new_item:
            item = cls()
        return item, new_item

    @classmethod
    def set_publish_objects(cls, ids, state):
        cls.set_bool_on_objects(ids, "published", state)

    @classmethod
    def set_bool_on_objects(cls, ids, attr, value):
        cls.objects.filter(id__in=ids).update(**{attr: value})

    @classmethod
    def delete_objects(cls, ids):
        for id in ids:
            try:
                item = cls.objects.get(id=id)
                item.delete()
            except cls.DoesNotExist:
                pass

    @classmethod
    def normalize_order(cls, filter=None):
        items = cls.objects.all() if filter == None else cls.objects.filter(filter)
        for n, item in enumerate(items):
            item.order = n
            item.save()


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username,  password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = MyUserManager.normalize_email(email)
        user = self.create_user(
            email,
            username,
            password,
        )

        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserTypeChoices(Enum):
    ADMIN = 0
    ENGINEER = 1
    SUPERVISOR = 2
    OPERATOR = 3


class CustomUser(AbstractBaseUser, AdminSetter):
    username = models.CharField(max_length=255, validators=[RegexValidator(
        regex=USERNAME_REGEX,
        message='Username must be Alphanumeric or contain any of the following ". @ + -"',
        code='invalid username'
    )], unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    company = models.ForeignKey("Company", blank=True, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        'staff status', default=False, help_text='Designates whether the user can log into this admin site.')
    ADMIN = 0
    ENGINEER = 1
    SUPERVISOR = 2
    OPERATOR = 3

    USER_TYPE_CHOICES = (
        (OPERATOR, 'operator'),
        (SUPERVISOR, 'supervisor'),
        (ENGINEER, 'engineer'),
        (ADMIN, 'admin'),
    )

    user_type = models.PositiveSmallIntegerField(default=ADMIN, choices=USER_TYPE_CHOICES)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    @staticmethod
    def permission_method(group, action, permissions, template):
        user_permission = False
        if action == 'view':
            user_permission = permissions[group+str('_')+template + str('_view')]
        elif action == 'edit':
            user_permission = permissions[group+str('_')+template + str('_edit')]
        elif action == 'delete':
            user_permission = permissions[group+str('_')+template + str('_delete')]
        elif action == 'dashboard':
            user_permission = permissions[group+str('_')+template + str('_dashboard')]
        return user_permission

    def can_access(self, user_type, template, action):
        """
        :param user_type: requested user permission
        :param template: template
        :param action: action
        :return: value of requested user permission
        """
        try:
            user_permission = False
            if user_type == self.ENGINEER:
                permissions = UserRoleTemplates.objects.values(
                    'engineer_company_view', 'engineer_company_edit', 'engineer_company_delete', 'engineer_device_view',
                    'engineer_device_edit', 'engineer_device_delete', 'engineer_product_view', 'engineer_product_edit',
                    'engineer_product_delete', 'engineer_users_view', 'engineer_users_edit', 'engineer_users_delete',
                    'engineer_administration_dashboard', 'operator_product_edit')[0]
                user_permission = self.permission_method('engineer', action, permissions, template)

            elif user_type == self.SUPERVISOR:
                permissions = UserRoleTemplates.objects.values(
                    'supervisor_company_view', 'supervisor_company_edit', 'supervisor_company_delete',
                    'supervisor_device_view', 'supervisor_device_edit', 'supervisor_device_delete',
                    'supervisor_product_view', 'supervisor_product_edit', 'supervisor_product_delete',
                    'supervisor_users_view', 'supervisor_users_edit', 'supervisor_users_delete',
                    'supervisor_administration_dashboard', 'operator_product_edit')[0]
                user_permission = self.permission_method('supervisor', action, permissions, template)

            elif user_type == self.OPERATOR:
                permissions = UserRoleTemplates.objects.values(
                    'operator_company_view', 'operator_company_edit', 'operator_company_delete',
                    'operator_device_view', 'operator_device_edit', 'operator_device_delete',
                    'operator_product_view', 'supervisor_product_edit', 'operator_product_delete',
                    'operator_product_edit', 'operator_users_view', 'operator_users_edit', 'operator_users_delete',
                    'operator_administration_dashboard')[0]

                user_permission = self.permission_method('operator', action, permissions, template)
            elif user_type == self.ADMIN:
                return True
            return user_permission
        except Exception as e:
            print(e)
            return False


def engineer_user_role_template():
    return UserRolePermissions.ENGINEER.value


def supervisor_user_role_template():
    return UserRolePermissions.SUPERVISOR.value


def operator_user_role_template():
    return UserRolePermissions.OPERATOR.value


class UserRoleTemplates(models.Model):
    # Supervisor user role definition
    supervisor_company_view = models.BooleanField(default=False)
    supervisor_company_edit = models.BooleanField(default=True)
    supervisor_company_delete = models.BooleanField(default=True)
    supervisor_device_view = models.BooleanField(default=True)
    supervisor_device_edit = models.BooleanField(default=True)
    supervisor_device_delete = models.BooleanField(default=True)
    supervisor_product_view = models.BooleanField(default=True)
    supervisor_product_edit = models.BooleanField(default=True)
    supervisor_product_delete = models.BooleanField(default=True)
    supervisor_users_view = models.BooleanField(default=True)
    supervisor_users_edit = models.BooleanField(default=True)
    supervisor_users_delete = models.BooleanField(default=True)
    supervisor_administration_dashboard = models.BooleanField(default=True)

    # Engineer user role definition
    engineer_company_view = models.BooleanField(default=True)
    engineer_company_edit = models.BooleanField(default=True)
    engineer_company_delete = models.BooleanField(default=True)
    engineer_device_view = models.BooleanField(default=True)
    engineer_device_edit = models.BooleanField(default=True)
    engineer_device_delete = models.BooleanField(default=True)
    engineer_product_view = models.BooleanField(default=True)
    engineer_product_edit = models.BooleanField(default=True)
    engineer_product_delete = models.BooleanField(default=True)
    engineer_users_view = models.BooleanField(default=False)
    engineer_users_edit = models.BooleanField(default=False)
    engineer_users_delete = models.BooleanField(default=False)
    engineer_administration_dashboard = models.BooleanField(default=False)

    # Operator user role definition
    operator_company_view = models.BooleanField(default=False)
    operator_company_edit = models.BooleanField(default=False)
    operator_company_delete = models.BooleanField(default=False)
    operator_device_view = models.BooleanField(default=False)
    operator_device_edit = models.BooleanField(default=False)
    operator_device_delete = models.BooleanField(default=False)
    operator_product_view = models.BooleanField(default=False)
    operator_product_edit = models.BooleanField(default=False)
    operator_product_delete = models.BooleanField(default=False)
    operator_users_view = models.BooleanField(default=False)
    operator_users_edit = models.BooleanField(default=False)
    operator_users_delete = models.BooleanField(default=False)
    operator_administration_dashboard = models.BooleanField(default=False)


class Company(AdminSetter, models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    note = models.TextField(max_length=250, default="")
    enabled = models.BooleanField(default=True)
    city = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=200, default="")
    access = models.ForeignKey("CompanyAccess", on_delete=models.DO_NOTHING, null=True)
    timezone = models.CharField(max_length=50, default="Europe/Zagreb")
    logo = models.ImageField(upload_to='logo', default='logo/logo.png')
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING, blank=True, null=True,)

    class Meta:
        db_table = 'administration_companies'
        ordering = ["name"]


class CompanyAccess(models.Model):
    device_tracking = models.BooleanField(default=False)
    product_tracking = models.BooleanField(default=False)

    class Meta:
        db_table = 'administration_company_access'


class Device(AdminSetter, models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    active = models.BooleanField(default=False)
    pid = models.CharField(max_length=45, default="")
    type = models.CharField(max_length=255, default="")
    serial_number = models.CharField(max_length=255, default="")
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING, blank=True, null=True,)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)


class Product(AdminSetter, models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    active = models.BooleanField(default=False)
    type = models.CharField(max_length=255, default="")
    description = models.CharField(max_length=255, default="")
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)


class RescanRobotMachine(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    robot = models.ForeignKey("robots_machine.Robots", on_delete=models.DO_NOTHING, null=True)
    rescan_status = models.BooleanField(default=False)
    activate_rescan = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    note = models.CharField(max_length=255, default="")

    class Meta:
        db_table = 'administration_rescan_robot_machine'


class Notification(AdminSetter, models.Model):
    email1 = models.EmailField(max_length=100)
    email2 = models.EmailField(max_length=100, blank=True)
    email3 = models.EmailField(max_length=100, blank=True)
    email4 = models.EmailField(max_length=100, blank=True)
    email5 = models.EmailField(max_length=100, blank=True)
    error = models.BooleanField(default=False)
    warning = models.BooleanField(default=False)
    info = models.BooleanField(default=False)
    robot_activity = models.PositiveSmallIntegerField(blank=True, null=True)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
