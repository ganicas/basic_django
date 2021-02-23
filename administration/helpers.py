from django.utils import timezone
import sys
import traceback

from django.contrib.auth.models import User

from administration.models import CustomUser, Company, Device, Product, UserTypeChoices, Notification


def get_users(user):
    user_list = []
    results = CustomUser.objects.all()
    name_link = u'<a class="denied_link" href="{2}/api/edit/user/{0}/">{1}</a>'
    button_on = u'<button type="button" id ="btn" class="btn btn-success" name="{0}"><i>Enabled</i></button>'
    button_off = u'<button type="button" class="btn btn-secondary" name="{0}"><i></i>Disabled</button>'
    delete = '<a type="button" class="btn btn-danger" id="{0}" href="#"><i class="sy_remove"></i>Delete</a>'
    for result in results:
        try:
            company_object = result.company
            role_id = result.user_type
            role = CustomUser.objects.get(id=result.id)
            row = list()
            row.append(name_link.format(result.id, result.username, ''))
            row.append(result.email)

            if company_object:
                company = result.company.name
                row.append(company)
            else:
                row.append('-')
            if role:
                role_value = role.user_type
                user_role_choices = {}
                choices_dict = {}
                for k, v in CustomUser.USER_TYPE_CHOICES:
                    user_role_choices[k] = v
                row.append(user_role_choices[role_value])
            else:
                row.append('Not defined role !')
            date = ''
            if result.last_login:
                from django.utils import timezone
                date = timezone.localtime(result.last_login)
                date = date.isoformat(' ')[:16]
            row.append(date)

            if result.id == user.id:
                row.append("")
            else:
                if result.is_active:
                    row.append(button_on.format(result.id))
                else:
                    row.append(button_off.format(result.id))
            row.append(delete.format(result.id))
            user_list.append(row)
        except Exception as e:
            print(e)
    return user_list


def get_company(company):
    company_list = []
    results = Company.objects.all()
    name_link = u'<a class="denied_link" href="{2}/api/edit/company/{0}/">{1}</a>'
    button_on = u'<button type="button" id ="btn" class="btn btn-success" name="{0}"><i>Enabled</i></button>'
    button_off = u'<button type="button" class="btn btn-secondary" name="{0}"><i></i>Disabled</button>'
    delete = '<a type="button" class="btn btn-danger" id="{0}" href="#"><i class="sy_remove"></i>Delete</a>'
    for result in results:
        try:
            row = list()
            row.append(name_link.format(result.id, result.name, ''))
            row.append(result.address)
            row.append(result.city)
            row.append(result.phone)
            row.append(result.email)
            row.append(result.note)
            if result.product:
                row.append(result.product.name)
            else:
                row.append("There is no company added yet!")
            if result.enabled:
                row.append(button_on.format(result.id))
            else:
                row.append(button_off.format(result.id))
            row.append(delete.format(result.id))
            company_list.append(row)
        except Exception as e:
            print(e)
    return company_list


def get_device(device):
    device_list = []
    results = Device.objects.all()
    name_link = u'<a class="denied_link" href="{2}/api/edit/device/{0}/">{1}</a>'
    button_on = u'<button type="button" id ="btn" class="btn btn-success" name="{0}"><i>Enabled</i></button>'
    button_off = u'<button type="button" class="btn btn-secondary" name="{0}"><i></i>Disabled</button>'
    delete = '<a type="button" class="btn btn-danger" id="{0}" href="#"><i class="sy_remove"></i>Delete</a>'
    for result in results:
        try:
            row = list()
            row.append(name_link.format(result.id, result.name, ''))
            row.append(result.serial_number)
            row.append(result.type)
            row.append(result.pid)
            if result.product:
                row.append(result.product.name)
            else:
                row.append("There is no device added yet!")
            if result.active:
                row.append(button_on.format(result.id))
            else:
                row.append(button_off.format(result.id))
            row.append(delete.format(result.id))
            device_list.append(row)
        except Exception as e:
            print(e)
    return device_list


def get_product(device):
    product_list = []
    results = Product.objects.all()
    name_link = u'<a class="denied_link" href="{2}/api/edit/product/{0}/">{1}</a>'
    button_on = u'<button type="button" id ="btn" class="btn btn-success" name="{0}"><i>Enabled</i></button>'
    button_off = u'<button type="button" class="btn btn-secondary" name="{0}"><i></i>Disabled</button>'
    delete = '<a type="button" class="btn btn-danger" id="{0}" href="#"><i class="sy_remove"></i>Delete</a>'
    for result in results:
        try:
            row = list()
            row.append(name_link.format(result.id, result.name, ''))
            row.append(result.description)
            row.append(result.type)

            if result.active:
                row.append(button_on.format(result.id))
            else:
                row.append(button_off.format(result.id))
            row.append(delete.format(result.id))
            product_list.append(row)
        except Exception:
            pass
    return product_list


def remove_user(id, user):

    try:
        u = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return u"User doesn't exist!"

    if u.is_active:
        return u"User is enabled!"

    u.delete()

    return 1


def remove_company(id, user):

    try:
        c = Company.objects.get(id=id)
    except Company.DoesNotExist:
        return u"Company doesn't exist!"

    if c.enabled:
        return u"Company is enabled!"

    c.delete()

    return 1


def remove_device(id, user):

    try:
        c = Device.objects.get(id=id)
    except Device.DoesNotExist:
        return u"Device doesn't exist!"

    if c.active:
        return u"Device is enabled!"

    c.delete()

    return 1


def remove_notification(id, user):

    try:
        c = Notification.objects.get(id=id)
    except Notification.DoesNotExist:
        return u"Device doesn't exist!"

    if c.active:
        return u"Device is enabled!"

    c.delete()

    return 1


def remove_product(id, user):

    try:
        c = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return u"Product doesn't exist!"

    if c.active:
        return u"Product is enabled!"
    try:
        c.delete()
    except Exception as e:
        return "This is destructive operation, can't delete product, description: " +str(e)

    return 1


def admin_user_changes(request_post, request_user):
    from administration.models import CustomUser

    try:
        request_dict = dict()
        for key in request_post:
            request_dict[key] = request_post[key]

        results = CustomUser.objects.filter(id=request_dict['id'])
        for result in results:
            if request_dict['name'] == 'enable':
                result.set_bool('is_active', True)
                result.save()
            elif request_dict['name'] == 'disable':
                result.set_bool('is_active', False)
                result.save()
            elif request_dict['name'] == 'delete':
                result.delete()

        return True
    except Exception as e:
        # print e
        return False


def admin_company_changes(request_post, request_user):
    from administration.models import CustomUser

    try:
        request_dict = dict()
        for key in request_post:
            request_dict[key] = request_post[key]

        results = Company.objects.filter(id=request_dict['id'])
        for result in results:
            if request_dict['name'] == 'enable':
                result.set_bool('enabled', True)
                result.save()
            elif request_dict['name'] == 'disable':
                result.set_bool('enabled', False)
                result.save()
            elif request_dict['name'] == 'delete':
                result.delete()

        return True
    except Exception as e:
        print(e)
        return False


def admin_product_changes(request_post, request_user):
    from administration.models import Product

    try:
        request_dict = dict()
        for key in request_post:
            request_dict[key] = request_post[key]

        results = Product.objects.filter(id=request_dict['id'])
        for result in results:
            if request_dict['name'] == 'enable':
                result.set_bool('active', True)
                result.save()
            elif request_dict['name'] == 'disable':
                result.set_bool('active', False)
                result.save()
            elif request_dict['name'] == 'delete':
                result.delete()

        return True
    except Exception as e:
        print(e)
        return False


def admin_device_changes(request_post, request_user):
    from administration.models import Device

    try:
        request_dict = dict()
        for key in request_post:
            request_dict[key] = request_post[key]

        results = Device.objects.filter(id=request_dict['id'])
        for result in results:
            if request_dict['name'] == 'enable':
                result.set_bool('active', True)
                result.save()
            elif request_dict['name'] == 'disable':
                result.set_bool('active', False)
                result.save()
            elif request_dict['name'] == 'delete':
                result.delete()

        return True
    except Exception as e:
        print(e)
        return False


def admin_notification_changes(request_post, request_user):
    try:
        request_dict = dict()
        for key in request_post:
            request_dict[key] = request_post[key]

        results = Notification.objects.filter(id=request_dict['id'])
        for result in results:
            if request_dict['name'] == 'enable':
                result.set_bool('active', True)
                result.save()
            elif request_dict['name'] == 'disable':
                result.set_bool('active', False)
                result.save()
            elif request_dict['name'] == 'delete':
                result.delete()

        return True
    except Exception as e:
        print(e)
        return False


def get_notification(notification):
    notification_list = []
    results = Notification.objects.all()
    button_on = u'<button type="button" id ="btn" class="btn btn-success" name="{0}"><i>Enabled</i></button>'
    button_off = u'<button type="button" class="btn btn-secondary" name="{0}"><i></i>Disabled</button>'
    delete = '<a type="button" class="btn btn-danger" id="{0}" href="#"><i class="sy_remove"></i>Delete</a>'
    for result in results:
        try:
            row = list()
            row.append(result.email1)
            if not result.email2:
                row.append('-')
            else:
                row.append(result.email2)

            if not result.email3:
                row.append('-')
            else:
                row.append(result.email3)

            if not result.email4:
                row.append('-')
            else:
                row.append(result.email4)
            if not result.email5:
                row.append('-')
            else:
                row.append(result.email5)
            if result.error:
                row.append('Enabled')
            else:
                row.append('Disabled')
            if result.warning:
                row.append('Enabled')
            else:
                row.append('Disabled')
            if result.info:
                row.append('Enabled')
            else:
                row.append('Disabled')
            if not result.robot_activity:
                row.append('-')
            else:
                row.append(str(result.robot_activity)+str('m'))
            if result.active:
                row.append(button_on.format(result.id))
            else:
                row.append(button_off.format(result.id))
            row.append(delete.format(result.id))
            notification_list.append(row)
        except Exception as e:
            print(e)
    print(notification_list)
    return notification_list
