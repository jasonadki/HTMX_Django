from django.urls import path, include

from rest_framework.routers import DefaultRouter


# from rest_framework_simplejwt.views

from .views import *



router = DefaultRouter()
router.register('', UserViewSet, basename='accounts')

urlpatterns = [
    path('user/', UserDetail.as_view(), name='userdetail'),
    path('get_account/', get_account, name='get_account'),
    # path('logout/', LogoutView.as_view(), name='logout'),


    
    path('process_login/', process_login_view, name='process_login'),
    # path('home/', home_view, name='home'),
    path('display_logout/', logout_view, name='display_logout'),
    path('upload_profile_picture/', upload_profile_picture, name='upload_profile_picture'),
    # path('profile/', profile_view, name='profile'),
    # path('signup/', signup_view, name='signup'),
    # path('create_account/', create_account_view, name='create_account'),
    # path('login/', display_login_view, name='display_login'),

    path('', include(router.urls)),
]
