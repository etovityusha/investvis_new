from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    name = 'portfolio'
    verbose_name = 'Портфель'

    def ready(self):
        import portfolio.signals
