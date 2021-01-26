from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # fieldsets = [
    #     (None, {'fields': ('email', 'password')}),
    #     ('Personal info', {'fields': ('title', 'first_name', 'last_name', 'phone_number', 'email','cms_logo','module_list_base_url','project_name')}),
    #     (
    #         'Permissions',
    #         {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}
    #     ),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    # ]
    # add_fieldsets = [
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'username', 'password1', 'password2'),
    #     }),
    # ]
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    ordering = ('email',)
