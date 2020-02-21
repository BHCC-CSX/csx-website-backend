from rest_framework import routers
from .api import ProjectViewSet

from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register('api', ProjectViewSet, 'projects')

urlpatterns = [
    path('', include(router.urls)),
]
