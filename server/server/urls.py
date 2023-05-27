from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework_simplejwt.views import \
    TokenRefreshView,\
    TokenObtainPairView
from .yasg import schema_view


API_PREFIX = 'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [
    # for deploy
    # re_path(r".*", TemplateView.as_view(template_name="index.html")),
]
