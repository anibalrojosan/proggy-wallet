from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")
    list_filter = ("created_at",)
    search_fields = ("user__username", "user__email")
    readonly_fields = ("created_at",)
