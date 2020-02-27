from mysite.site_hooks import RouterHook
from mysite import hooks
from .urls import router


@hooks.register('router_hook')
def register_router():
    return RouterHook(router)
