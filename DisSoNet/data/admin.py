from django.contrib import admin
from data import models
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(DUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'firstName', 'lastName', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'guid',)}),
        ('Personal info',
         {'fields': ('firstName', 'lastName',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'firstName', 'lastName')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Friends)
admin.site.register(models.Category)
admin.site.register(models.GitHub)
