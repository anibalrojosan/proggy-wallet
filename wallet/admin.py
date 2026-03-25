from django.contrib import admin

from .models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "created_at")
    search_fields = ("user__username", "user__email")
    list_filter = ("created_at",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "from_user", "to_user", "type", "amount", "created_at")
    list_filter = ("type", "created_at")
    search_fields = ("from_user__username", "to_user__username", "description")
    readonly_fields = ("created_at",)
