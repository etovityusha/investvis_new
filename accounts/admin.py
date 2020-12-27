from django.contrib import admin

from . import models


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'open_portfolio', 'analytics_currency',)


admin.site.register(models.Profile, ProfileAdmin)
