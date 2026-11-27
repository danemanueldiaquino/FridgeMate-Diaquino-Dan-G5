from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import FridgeItem, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('FridgeMate Information', {
            'fields': (
                'role',
                'contact_number',
                'profile_photo',
            )
        }),
    )

    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_active',
    )


@admin.register(FridgeItem)
class FridgeItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'zone', 'quantity', 'unit', 'expiry_date')
    list_filter = ('zone', 'expiry_date')
    search_fields = ('name', 'owner__username', 'owner__email')