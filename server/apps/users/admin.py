from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    search_fields = ('email',)
    list_filter = ('is_active',)
    ordering = ('-created_at',)
    list_display = (
        'email', 'created_at', 'is_active'
    )
    fieldsets = (
        (None, {'fields': ('email', 'description',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups')}),
        ('Other', {'fields': ('id', 'created_at', 'updated_at')})
    )
    readonly_fields = ('id', 'created_at', 'updated_at')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'description', 'is_active', 'is_staff')}
         ),
    )
