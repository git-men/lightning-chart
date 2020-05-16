from django.apps import AppConfig


class ChartConfig(AppConfig):
    name = 'chart'

    def ready(self):
        from . import signals
