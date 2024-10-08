from django.apps import AppConfig


class PromotionalSiteConfig(AppConfig):
    name = "bc.promotional"

    def ready(self):
        from . import signal_handlers  # noqa F401
