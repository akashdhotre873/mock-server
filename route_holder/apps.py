from django.apps import AppConfig

from . import urls


class RouteHolderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "route_holder"
    urls.reloadUrls()
