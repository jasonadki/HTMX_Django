from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from accounts.views import create_account_view, display_login_view, home_view, profile_view, signup_view # import home_view


from django.conf import settings
from django.conf.urls.static import static

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

    path('home/', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('signup/', signup_view, name='signup'),
    path('create_account/', create_account_view, name='create_account'),
    path('login/', display_login_view, name='display_login'),


    path("accounts/", include("accounts.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
