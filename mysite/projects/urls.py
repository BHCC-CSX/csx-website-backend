from rest_framework import routers
from .api import ProjectViewSet

from django.urls import path, include
from mysite.mysite.urls import router as core_router
from . import views

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, 'projects')
core_router.registry.extend(router.registry)

urlpatterns = [
    path('', include(router.urls)),
]
