from django.contrib import admin, messages
from django.http.request import HttpRequest
from django.db.models import QuerySet


class ReadOnlyFieldsAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
    )


class SoftDeletionAdmin(admin.ModelAdmin):
    actions = (
        'soft_delete',
        'restore',
    )
    
    def soft_delete(self, request: HttpRequest,
                    queryset: QuerySet) -> None:
        queryset.update(is_active=False)
        messages.success(
            request, 'Selected entities are deleted')

    def restore(self, request: HttpRequest,
                    queryset: QuerySet) -> None:
        queryset.update(is_active=True)
        messages.success(
            request, 'Selected entities are restored')

    soft_delete.short_description = 'Soft Deletion'
    restore.short_description = 'Restoring'


class BaseAdmin(ReadOnlyFieldsAdmin, SoftDeletionAdmin):
    pass
