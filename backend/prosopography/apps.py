from django.apps import AppConfig


class ProsopographyConfig(AppConfig):
    name = 'prosopography'

    def ready(self):
        import prosopography.signals.handlers
