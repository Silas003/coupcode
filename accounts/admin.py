from django.contrib import admin
from . import models

# Register your models here.


class ProfileAdmin(admin.TabularInline):
    model = models.Profile
    extra = 1


@admin.register(models.CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id","username", "email"]
    list_filter = [
        "username",
        "email",
    ]
    search_fields = [
        "username",
        "email",
    ]

    inlines = [ProfileAdmin]
