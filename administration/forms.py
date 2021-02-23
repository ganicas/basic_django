from io import StringIO
from django.contrib.admin.views import autocomplete
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from django import forms
from django.core.validators import RegexValidator
from administration.models import CustomUser, USERNAME_REGEX, Company, CompanyAccess, Device, Product, \
    UserRoleTemplates, Notification
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

# If you don't do this you cannot use Bootstrap CSS


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30, validators=[RegexValidator(
        regex=USERNAME_REGEX,
        message='Username must be Alphanumeric or contain any of the following ". @ + -"',
        code='invalid username'
    )], widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'name': 'password'}))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user_obj = User.objects.filter(username=username).first()

        """
        # initial way of checking
        the_user = authenticate(username=username, password=password)
        if not the_user:
            raise forms.ValidationError("Invalid credentials")
        """
        # another way of checking
        if not user_obj:
            raise forms.ValidationError("Invalid credentials")
        else:
            if not user_obj.check_password(password):
                # log auth tries
                raise forms.ValidationError("Invalid credentials")
        return super(UserLoginForm, self).clean()

    """
    # checking per one field
    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_qs = User.objects.filter(username=username)
        user_exists = user_qs.exists()
        if not user_exists and user_qs.count() != 1:
            return forms.ValidationError("Invalid credentials")
        return username
    """


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'name': 'password'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'name': 'password'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'company')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('company', 'email', 'password', 'username', 'user_type', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileForm(forms.ModelForm):
    model = User


class AddUser(forms.Form):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    company = forms.CharField(max_length=254)
    user_type = forms.IntegerField()


class CustomModelChoiceFieldUser(forms.ModelChoiceField):
    def label_from_instance(self, user_object):
        user_role = {}

        for k, v in CustomUser.USER_TYPE_CHOICES:
            user_role[k] = str(v)
        return user_role


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, company_object):
        return company_object.name


class UserRoleFields(forms.ModelChoiceField):
    def label_from_instance(self, company_object):
        print(company_object.supervisor)
        return company_object.supervisor


class AddUserForm(UserCreationForm):
    """
    Create new user form, this is django model form.
    """

    company_data = Company.objects.all()

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'username',
        }
    ))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'first name',
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'last name',
        }
    ))
    user_type = forms.CharField(widget=forms.Select(
        choices=CustomUser.USER_TYPE_CHOICES,
        attrs={
            'class': 'form-control',
            'placeholder': 'user_type',
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'email',
        }
    ))
    company = CustomModelChoiceField(required=False, queryset=Company.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'company',
        }
    ))

    field_order = ['first_name', 'last_name', 'last_name', 'username', 'email', 'company', 'user_type', 'password1', 'password2']


class EditUserForm(UserChangeForm):
    """
    Edit user form, this is django model form.
    """
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'username',
        }
    ))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'first name',
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'last name',
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'email',
        }
    ))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'last_name', 'username', 'email', 'email', 'password']


class EditCustomUsers(UserChangeForm):
    company_data = Company.objects.all()

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'username',
        }
    ))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'first name',
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'last name',
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'email',
        }
    ))
    company = CustomModelChoiceField(queryset=Company.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'company',
        }
    ))

    user_type = forms.CharField(widget=forms.Select(
        choices=CustomUser.USER_TYPE_CHOICES,
        attrs={
            'class': 'form-control',
            'placeholder': 'user_type',
        }
    ))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'last_name', 'username', 'email', 'email', 'company', 'user_type', 'password']

    def clean(self):
        self.validate_unique()
        return self.cleaned_data


class CreateCompany(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'company name',
        }
    ))
    address = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'address',
        }
    ))
    city = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'city',
        }
    ))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'phone',
        }
    ))
    note = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'note',
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'email',
        }
    ))
    product = CustomModelChoiceField(required=False, queryset=Product.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'product',
        }
    ))

    class Meta:
        model = Company
        fields = ['name', 'address', 'city', 'phone', 'email', 'note', 'product']

    def clean(self):
        self.validate_unique()
        return self.cleaned_data


class CreateDevice(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'device name',
        }
    ))
    serial_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'serial number',
        }
    ))
    type = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'device type',
        }
    ))
    pid = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'device pid',
        }
    ))
    product = CustomModelChoiceField(required=False, queryset=Product.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'product',
        }
    ))

    class Meta:
        model = Device
        fields = ['name', 'serial_number', 'type', 'pid', 'product']

    def clean_product(self):
        return self.cleaned_data['product'] or None


class CreateProduct(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'product name',
        }
    ))
    description = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'product description',
        }
    ))
    type = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'product type',
        }
    ))

    class Meta:
        model = Product
        fields = ['name', 'description', 'type']

    def clean(self):
        self.validate_unique()
        return self.cleaned_data


class UserRoleForm(forms.ModelForm):
    supervisor_company_view = forms.BooleanField(required=False)
    supervisor_company_edit = forms.BooleanField(required=False)
    supervisor_company_delete = forms.BooleanField(required=False)
    supervisor_device_view = forms.BooleanField(required=False)
    supervisor_device_edit = forms.BooleanField(required=False)
    supervisor_device_delete = forms.BooleanField(required=False)
    supervisor_product_view = forms.BooleanField(required=False)
    supervisor_product_edit = forms.BooleanField(required=False)
    supervisor_product_delete = forms.BooleanField(required=False)
    supervisor_users_view = forms.BooleanField(required=False)
    supervisor_users_edit = forms.BooleanField(required=False)
    supervisor_users_delete = forms.BooleanField(required=False)
    supervisor_administration_dashboard = forms.BooleanField(required=False)
    engineer_company_view = forms.BooleanField(required=False)
    engineer_company_edit = forms.BooleanField(required=False)
    engineer_company_delete = forms.BooleanField(required=False)
    engineer_device_view = forms.BooleanField(required=False)
    engineer_device_edit = forms.BooleanField(required=False)
    engineer_device_delete = forms.BooleanField(required=False)
    engineer_product_view = forms.BooleanField(required=False)
    engineer_product_edit = forms.BooleanField(required=False)
    engineer_product_delete = forms.BooleanField(required=False)
    engineer_users_view = forms.BooleanField(required=False)
    engineer_users_edit = forms.BooleanField(required=False)
    engineer_users_delete = forms.BooleanField(required=False)
    engineer_administration_dashboard = forms.BooleanField(required=False)
    operator_company_view = forms.BooleanField(required=False)
    operator_company_edit = forms.BooleanField(required=False)
    operator_company_delete = forms.BooleanField(required=False)
    operator_device_view = forms.BooleanField(required=False)
    operator_device_edit = forms.BooleanField(required=False)
    operator_device_delete = forms.BooleanField(required=False)
    operator_product_view = forms.BooleanField(required=False)
    operator_product_edit = forms.BooleanField(required=False)
    operator_product_delete = forms.BooleanField(required=False)
    operator_users_view = forms.BooleanField(required=False)
    operator_users_edit = forms.BooleanField(required=False)
    operator_users_delete = forms.BooleanField(required=False)
    operator_administration_dashboard = forms.BooleanField(required=False)

    class Meta:
        model = UserRoleTemplates
        fields = [
            'supervisor_company_view',
            'supervisor_company_edit',
            'supervisor_company_delete',
            'supervisor_device_view',
            'supervisor_device_edit',
            'supervisor_device_delete',
            'supervisor_product_view',
            'supervisor_product_edit',
            'supervisor_product_delete',
            'supervisor_users_view',
            'supervisor_users_edit',
            'supervisor_users_delete',
            'supervisor_administration_dashboard',
            'engineer_company_view',
            'engineer_company_edit',
            'engineer_company_delete',
            'engineer_device_view',
            'engineer_device_edit',
            'engineer_device_delete',
            'engineer_product_view',
            'engineer_product_edit',
            'engineer_product_delete',
            'engineer_users_view',
            'engineer_users_edit',
            'engineer_users_delete',
            'engineer_administration_dashboard',
            'operator_company_view',
            'operator_company_edit',
            'operator_company_delete',
            'operator_device_view',
            'operator_device_edit',
            'operator_device_delete',
            'operator_product_view',
            'operator_product_edit',
            'operator_product_delete',
            'operator_users_view',
            'operator_users_edit',
            'operator_users_delete',
            'operator_administration_dashboard'
        ]


class RobotNotification(forms.ModelForm):
    email1 = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'email 1 mandatory',
        }
    ))
    email2 = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'email 2',
        }
    ), required=False)
    email3 = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'email 3',
        }
    ), required=False)
    email4 = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'email 4',
        }
    ), required=False)
    email5 = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'email 5',
        }
    ), required=False)
    error = forms.BooleanField(required=False)
    warning = forms.BooleanField(required=False)
    info = forms.BooleanField(required=False)
    robot_activity = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'notification activity (min)',
        }
    ), required=False)

    class Meta:
        model = Notification
        fields = ['email1', 'email2', 'email3', 'email4', 'email5', 'error', 'warning', 'info', 'robot_activity']

    def clean(self):
        self.validate_unique()
        return self.cleaned_data

