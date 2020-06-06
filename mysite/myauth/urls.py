from rest_framework import routers
from django.urls import path, include
from django.contrib import admin
from .views import *
from rest_framework_simplejwt import views as jwt_views
admin.autodiscover()


urlpatterns = [
    path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserList.as_view()),
    path('user/', UserRegister.as_view()),
    path('user/<int:user_id>/', UserDetail.as_view()),
    path('groups/', Groups.as_view())
]