from django import forms
from administration.models import Product, Company, Device, RescanRobotMachine
from robots_machine.models import Robots


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, company_object):
        return company_object.name


class CreateRobot(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'robot name',
        }
    ))
    serial_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'robot serial number',
        }
    ))
    note = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'note',
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
    address = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'address',
        }
    ))
    product = CustomModelChoiceField(required=False, queryset=Product.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'product',
        }
    ))
    company = CustomModelChoiceField(required=False, queryset=Company.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'company',
        }
    ))

    robot_ip_address = forms.GenericIPAddressField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'robot ip address',
        }
    ))
    robot_username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'robot username',
        }
    ))
    robot_password = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'robot password',
        }
    ))
    planned_production_min = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'total time that equipment is excepted to produce (insert min)',
        }
    ))
    ideal_cycle_second = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'theoretical minimum part to produce one part (insert seconds)',
        }
    ))

    class Meta:
        model = Robots
        fields = ['name', 'serial_number', 'note', 'city', 'phone', 'address', 'product',  'company',
                  'robot_ip_address', 'robot_username', 'robot_password', 'planned_production_min',
                  'ideal_cycle_second']


class RescanRobotMachineForm(forms.ModelForm):
    start_date = forms.DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"], widget=forms.DateInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'start date format: Y-m-d H:M:S',

        },

    ))
    end_date = forms.DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"], widget=forms.DateInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'end date format: Y-m-d H:M:S',
        }
    ))
    robot = CustomModelChoiceField(required=False, queryset=Robots.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'company',
        }
    ))

    class Meta:
        model = RescanRobotMachine
        fields = ['start_date', 'end_date', 'robot']
