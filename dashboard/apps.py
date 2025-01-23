from django.apps import AppConfig

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        # Import signals to ensure they are connected when the app is ready
        import dashboard.signals
        print("Dashboard app signals connected")


