from io import StringIO

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.context_processors import csrf
from django.contrib.auth import login, get_user_model, logout

from administration.forms import UserProfileForm, AddUser, UserCreationForm, UserLoginForm, AddUserForm, EditUserForm, \
    EditCustomUsers, CreateCompany, CreateDevice, CreateProduct, UserRoleForm, RobotNotification
from administration.helpers import get_users, remove_user, admin_user_changes, get_company, remove_company, \
    admin_company_changes, get_device, remove_device, admin_device_changes, get_product, remove_product, \
    admin_product_changes, get_notification, admin_notification_changes, remove_notification
from administration.models import CustomUser, Company, Device, Product, UserRoleTemplates, MyUserManager
from proel.decorators import require_access

User = get_user_model()


@login_required(login_url="login/")
def main_administration(request):
    access = {'access': request.user.can_access(request.user.user_type, 'administration', 'dashboard')}
    return render(request, 'index.html', access)


@login_required(login_url="login/")
def about(request):
    access = {'access': request.user.can_access(request.user.user_type, 'administration', 'dashboard')}
    return render(request, 'core/navigation/about.html', access)


@login_required(login_url="login/")
def services(request):
    access = {'access': request.user.can_access(request.user.user_type, 'administration', 'dashboard')}
    return render(request, 'core/navigation/services.html', access)


@login_required(login_url="login/")
def contact(request):
    access = {'access': request.user.can_access(request.user.user_type, 'administration', 'dashboard')}
    return render(request, 'core/navigation/contact.html', access)


@login_required(login_url="login/")
def settings(request):
    access = {'access': request.user.can_access(request.user.user_type, 'administration', 'dashboard')}
    return render(request, 'administration/settings.html', access)


@login_required
@require_access('device', 'view')
def device_list(request):
    return render(request, 'administration/device.html', {})


@login_required
@require_access('product', 'view')
def product_list(request):
    return render(request, 'administration/product.html', {})


@login_required
@require_access('users', 'view')
def users(request):
    return render(request, 'administration/user.html', {})


@login_required
@require_access('dashboard', 'dashboard')
def dashboard(request):
    return render(request, 'administration/dashboard.html', {})


@login_required
@require_access('company', 'view')
def company_list(request):
    return render(request, 'administration/company.html', {})


@login_required
def rescan_robot_list(request):
    return render(request, 'robot_machine/rescan_robot.html', {})


@login_required(login_url="login/")
def notifications_auto_industry(request):
    return render(request, 'administration/notifications.html', {})


@login_required(login_url="login/")
def monitoring_auto_industry(request):
    return render(request, 'administration/monitoring.html', {})


def get_companies_for_user_list(user):
    user_object = CustomUser.objects.filter(first_name=user)
    if len(user_object):
        return user_object


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('user/profile/')
        else:
            user = request.user
            profile = user.id
            form = UserProfileForm(instance=profile)

        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render('user.html', args)


@login_required
@require_access('users', 'view')
def get_user_list(request):
    import json
    data = get_users(request.user)
    response = {"data": data}
    s = StringIO()
    json.dump(response, s)
    s.seek(0)

    return HttpResponse(s.read())


@login_required
@require_access('company', 'view')
def get_company_list(request):
    import json
    data = get_company(request.user)
    response = {"data": data}
    s = StringIO()
    json.dump(response, s)
    s.seek(0)

    return HttpResponse(s.read())


@login_required
@require_access('device', 'view')
def get_device_list(request):
    import json
    data = get_device(request.user)
    response = {"data": data}
    s = StringIO()
    json.dump(response, s)
    s.seek(0)

    return HttpResponse(s.read())


@login_required
@require_access('device', 'view')
def get_notification_list(request):
    import json
    data = get_notification(request.user)
    response = {"data": data}
    s = StringIO()
    json.dump(response, s)
    s.seek(0)

    return HttpResponse(s.read())


@login_required
@require_access('product', 'view')
def get_product_list(request):
    import json
    data = get_product(request.user)
    response = {"data": data}
    s = StringIO()
    json.dump(response, s)
    s.seek(0)

    return HttpResponse(s.read())


@login_required
@require_access('users', 'edit')
def create_user(request):
    form = AddUserForm(request.POST or None)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.user_type = form.data['user_type']
        if form.data['user_type'] == CustomUser.ADMIN:
            MyUserManager.create_superuser(
                email=form.data['email'],
                username=form.data['username'],
                password=form.data['password']
            )
        profile.save()
        form = AddUserForm()

    return render(request, "administration/add_new_user.html", {"form": form})


@login_required
@require_access('company', 'edit')
def create_company(request):
    form = CreateCompany(request.POST or None)
    if form.is_valid():
        form.save()
        form = CreateCompany()

    return render(request, "administration/add_new_company.html", {"form": form})


@login_required
@require_access('device', 'edit')
def create_device(request):
    form = CreateDevice(request.POST or None)
    if form.is_valid():
        form.save()
        form = CreateDevice()

    return render(request, "administration/add_new_device.html", {"form": form})


@login_required
def create_notification(request):
    form = RobotNotification(request.POST or None)
    if form.is_valid():
        form.save()
        form = RobotNotification()

    return render(request, "administration/add_new_notifications.html", {"form": form})


@login_required
@require_access('product', 'edit')
def create_product(request):
    form = CreateProduct(request.POST or None)
    if form.is_valid():
        form.save()
        form = CreateProduct()

    return render(request, "administration/add_new_product.html", {"form": form})


@login_required
def user_role(request):
    if request.method == 'POST':
        edit_form = UserRoleForm(request.POST, instance=UserRoleTemplates.objects.last())
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect('/role/templates')
    else:
        edit_form = UserRoleForm(instance=UserRoleTemplates.objects.last())
    return render(request, "administration/user_role.html", {"form": edit_form})


@login_required
@require_access('user', 'edit')
def update_user(request):
    if request.method == 'POST':
        edit_form = EditUserForm(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect('/api/user/user-profile')
    else:
        edit_form = EditUserForm(instance=request.user)
    return render(request, "administration/edit_user.html", {"edit_form": edit_form})


def change_password(request):
    if request.method == 'POST':
        change_password_form = PasswordChangeForm(data=request.POST, user=request.user)
        if change_password_form.is_valid():
            change_password_form.save()
            update_session_auth_hash(request, change_password_form.user)
            return HttpResponseRedirect('/api/user/user-profile')
        else:
            return HttpResponseRedirect('/api/user/change-password')
    else:
        change_password_form = PasswordChangeForm(user=request.user)
    return render(request, "administration/change_password.html", {"change_password_form": change_password_form})


def user_profile_form(request):
    if request.method == 'GET':
        user_data = CustomUser.objects.filter(id=request.user.id)
        if len(user_data):
            for x in user_data:
                user_info = {
                    'username': x.username,
                    'first_name': x.first_name,
                    'last_name': x.last_name,
                    'company': x.company.name if x.company else '',
                    'email': x.email
                }

                return render(request, "administration/user_profile.html", {"user_info": user_info})


def register(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save(commit=False)
        return HttpResponseRedirect("/login")
    return render(request, "registration/register.html", {'form': form})


def user_login(request, *args, **kwargs):

    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username_ = form.cleaned_data.get('username')
        user_obj = User.objects.get(username__iexact=username_)
        login(request, user_obj)
        return HttpResponseRedirect("/")
    return render(request, "registration/login.html", {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login")


def get_user_info(user_id, request_user):
    from administration.models import CustomUser

    if user_id:
        user = CustomUser.objects.get(id=user_id)
        company = user.company
        all_company = Company.objects.all().values_list('name', flat=True)
        user_dict = dict()

        user_dict['user_id'] = user.id
        user_dict['first_name'] = user.first_name
        user_dict['username'] = user.username
        user_dict['last_name'] = user.last_name
        user_dict['email'] = user.email
        user_dict['company'] = company.name if company else ""
        user_dict['enabled'] = user.is_active
        user_dict['all_company'] = list(all_company)
        return user_dict, user
    else:
        return None


@login_required
@require_access('users', 'edit')
def edit_user(request, id):
    target_user = CustomUser.objects.get(id=id)
    user, user_obj = get_user_info(id, request.user)

    if request.method == 'POST':
        edit_form = EditCustomUsers(request.POST, instance=CustomUser.objects.get(id=id))
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect('/user')
    else:
        edit_form = EditCustomUsers(instance=CustomUser.objects.get(id=id))
    return render(request, "administration/edit_custom_user.html", {"form": edit_form})


@login_required
@require_access('company', 'edit')
def edit_company(request, id):

    if request.method == 'POST':
        edit_form = CreateCompany(request.POST, instance=Company.objects.get(id=id))
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect('/company/list')
    else:
        edit_form = CreateCompany(instance=Company.objects.get(id=id))
    return render(request, "administration/edit_company.html", {"form": edit_form})


@login_required
@require_access('device', 'edit')
def edit_device(request, id):

    if request.method == 'POST':
        edit_form = CreateDevice(request.POST, instance=Device.objects.get(id=id))
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect('/device/list')
    else:
        edit_form = CreateDevice(instance=Device.objects.get(id=id))
    return render(request, "administration/edit_device.html", {"form": edit_form})


@login_required
@require_access('product', 'edit')
def edit_product(request, id):

    if request.method == 'POST':
        edit_form = CreateProduct(request.POST, instance=Product.objects.get(id=id))
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect('/product/list')
    else:
        edit_form = CreateProduct(instance=Product.objects.get(id=id))
    return render(request, "administration/edit_product.html", {"form": edit_form})


@login_required
@require_access('users', 'delete')
def user_delete(request):
    id = request.POST.get('id', 0)
    if id:
        error = remove_user(id, request.user)
        return HttpResponse(error)
    else:
        return HttpResponse("No id sent")


@login_required
@require_access('company', 'delete')
def company_delete(request):
    id = request.POST.get('id', 0)
    if id:
        error = remove_company(id, request.user)
        return HttpResponse(error)
    else:
        return HttpResponse("No id sent")


@login_required
@require_access('device', 'delete')
def device_delete(request):
    id = request.POST.get('id', 0)
    if id:
        error = remove_device(id, request.user)
        return HttpResponse(error)
    else:
        return HttpResponse("No id sent")


@login_required
@require_access('notification', 'delete')
def notification_delete(request):
    id = request.POST.get('id', 0)
    if id:
        error = remove_notification(id, request.user)
        return HttpResponse(error)
    else:
        return HttpResponse("No id sent")


@login_required
@require_access('product', 'delete')
def product_delete(request):
    id = request.POST.get('id', 0)
    if id:
        error = remove_product(id, request.user)
        return HttpResponse(error)
    else:
        return HttpResponse("No id sent")


@login_required
def user_admin_command(request):
    request_post = request.POST
    request_user = request.user

    if admin_user_changes(request_post, request_user):
        return HttpResponse(1)
    else:
        return HttpResponse(0)


@login_required
def user_admin_command_company(request):
    request_post = request.POST
    request_user = request.user

    if admin_company_changes(request_post, request_user):
        return HttpResponse(1)
    else:
        return HttpResponse(0)


@login_required
def user_admin_command_product(request):
    request_post = request.POST
    request_user = request.user

    if admin_product_changes(request_post, request_user):
        return HttpResponse(1)
    else:
        return HttpResponse(0)


@login_required
def user_admin_device_company(request):
    request_post = request.POST
    request_user = request.user

    if admin_device_changes(request_post, request_user):
        return HttpResponse(1)
    else:
        return HttpResponse(0)


@login_required
def user_admin_notification(request):
    request_post = request.POST
    request_user = request.user

    if admin_notification_changes(request_post, request_user):
        return HttpResponse(1)
    else:
        return HttpResponse(0)

