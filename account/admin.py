from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account, AccessToken


@admin.register(AccessToken)
class BookAdAdmin(admin.ModelAdmin):
    list_display = ('pk', 'account_type', 'token', 'token_expiration')
    search_fields = ('pk', 'token')
    readonly_fields = ('pk',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('pk', 'email', 'username', 'created', 'modified', 'is_admin', 'is_active')
    search_fields = ('pk', 'email', 'username')
    readonly_fields = ('pk', 'created', 'last_login',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
