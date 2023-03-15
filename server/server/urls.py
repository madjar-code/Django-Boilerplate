from django.contrib import admin
from django.urls import path, re_path
from .yasg import schema_view


API_PREFIX = 'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]