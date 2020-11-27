from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from NewsApp import models

class AppUserAdmin(UserAdmin):
    # Add fields to AppUser creation form on the admin site
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'is_superuser', 'is_staff', 'is_active',)}),
    )
    filter_horizontal = ()

# Register models for admin site.
admin.site.register(models.AppUser, AppUserAdmin)
admin.site.register(models.NewsArticle)
admin.site.register(models.NewsCategory)