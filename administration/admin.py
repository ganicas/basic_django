from django.contrib import admin

# Register your models here.
#from administration.models import CustomUser
#admin.site.register(CustomUser)


from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from administration.models import CustomUser


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'company', 'user_type',)
    list_filter = ('user_type',)
    fieldsets = (
        (None, {'fields': ('username', 'company', 'email', 'password',)}),
        #('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('user_type',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'company', 'password1', 'password2',)}
        ),
    )
    search_fields = ('email', 'username', 'company',)
    ordering = ('email', 'username', 'company',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)