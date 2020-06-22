from django.apps import AppConfig


class CurrenciesConfig(AppConfig):
    name = 'currencies'

    def ready(self):
        import currencies.signals  # noqa
