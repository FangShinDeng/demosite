from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from django.utils.translation import gettext, gettext_lazy as _
# # Register your models here.

def get_model_fields(model):
    return [field.name for field in model._meta.get_fields()]

class UserProfileAdmin(admin.ModelAdmin):
    list_display = get_model_fields(models.UserProfile)

admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)