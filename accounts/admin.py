from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from .models import User, OtpCode, PostalInfo


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name', 'phone_number','is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields':('name', 'phone_number', 'password')}),
        ('permissions', {'fields': ('is_active', 'is_admin', 'last_login')}),
    )

    add_fieldsets = (
        (None, {'fields':('name', 'phone_number', 'password1', 'password2')}),
    )

    search_fields = ('phone_number',)
    ordering = ('name',)
    filter_horizontal = ()

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(OtpCode)
admin.site.register(PostalInfo)


