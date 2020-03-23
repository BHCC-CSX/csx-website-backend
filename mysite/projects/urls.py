from rest_framework import routers
from .views import ProjectViewSet, ProjectImageView

from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(prefix='projects', viewset=ProjectViewSet, basename='projects')

urlpatterns = [
    path('', include(router.urls)),
]
