from rest_framework import routers
from django.urls import path, include
from django.contrib import admin
from .views import *
admin.autodiscover()


urlpatterns = [
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', UserList.as_view()),
    path('user/', UserRegister.as_view()),
    path('user/<int:user_id>/', UserDetail.as_view()),
    path('groups/', Groups.as_view())
]