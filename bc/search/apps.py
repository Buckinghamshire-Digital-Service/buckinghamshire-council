from django.apps import AppConfig


class SearchConfig(AppConfig):
    name = "bc.search"

    def ready(self):
        import bc.search.query  # noqa
        import bc.search.signal_handlers  # noqa
