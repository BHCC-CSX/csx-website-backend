from rest_framework import routers
from .views import ProjectViewSet

from django.urls import path, include

router = routers.DefaultRouter()
router.register(prefix='projects', viewset=ProjectViewSet, basename='projects')

urlpatterns = [
    path('', include(router.urls)),
]
