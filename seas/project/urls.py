from django.contrib import admin
from django.urls import include, path

from seas.project.config import RunEnvType, seas_config

urlpatterns = [
    path('api/v1/', include('seas.app.services.dispatch.dispatcher'), name="api"),
]

if seas_config.run_env_type == RunEnvType.development:
    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

    urlpatterns += [
        path('admin/', admin.site.urls),
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
