from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import LeebUserCreationForm, LeebUserChangeForm
from .models import LeebUser


class LeebUserAdmin(UserAdmin):
    add_form = LeebUserCreationForm
    form = LeebUserChangeForm
    model = LeebUser
    list_display = [
        "username",
        "email",
        "credit",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("credit",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("credit",)}),)


admin.site.register(LeebUser, LeebUserAdmin)
