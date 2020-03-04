from mysite.site_hooks import URLHook
from mysite import hooks
from .urls import urlpatterns


@hooks.register('url_hook')
def register_router():
    return URLHook(urlpatterns)
