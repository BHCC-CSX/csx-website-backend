"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .hooks import get_hooks

router = routers.DefaultRouter()

api_urls = []

apps = get_hooks("url_hook")
for app in apps:
    # print(app().reg.registry)
    api_urls += app().pats

apps = get_hooks("named_url_hook")
for app in apps:
    app_urls = app().pats
    api_urls += [path(app().prefix, include(app_urls))]


# Swagger Stuff
schema_view = get_schema_view(
   openapi.Info(
      title="CSX Backend API",
      default_version='v1',
      description="This API serves as the backend for the BHCC CSX website.",
      contact=openapi.Contact(email="contact@bhcsx.tech"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
static_url = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) if settings.MEDIA_URL else None

if static_url is not None:
    urlpatterns += static_url

