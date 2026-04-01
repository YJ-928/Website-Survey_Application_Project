from django.contrib import admin
from django.db import connection
from django.http import HttpResponse
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.conf.urls.static import static

# API Root Endpoint
def root_service_view(request):
    return HttpResponse(
        "Survey Application API Service is running",
        content_type="text/plain",
        status=200,
    )

# Health Check Endpoint
def health_check_view(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return HttpResponse(
            "OK",
            content_type="text/plain",
            status=200,
        )

    except Exception:
        return HttpResponse(
            "DB DOWN",
            content_type="text/plain",
            status=503,
        )

# Swagger / OpenAPI Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Survey Application API",
        default_version="v1",
        description="Admin, Invite, Survey and Dashboard APIs",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

# URL Patterns
urlpatterns = [
    # Root & Health
    path("", root_service_view),
    path("health/", health_check_view),

    # Django Admin
    path("admin/", admin.site.urls),

    # API routes
    path("api/", include("api.urls")),

    # Swagger / OpenAPI
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("api/docs/swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("api/docs/redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)