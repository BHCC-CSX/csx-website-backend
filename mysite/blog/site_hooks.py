from mysite.site_hooks import NamedURLHook
from mysite import hooks
from .urls import urlpatterns


@hooks.register('named_url_hook')
def register_patterns():
    return NamedURLHook(urlpatterns, "blog/")
