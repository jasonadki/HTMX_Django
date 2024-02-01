from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/', include('djoser.urls.jwt')),
    path('api/v1/token/obtain/', TokenObtainPairView.as_view(), name='token_create'),  # override jwt stock token
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # override jwt stock token
    path("accounts/", include("accounts.urls")),
]
