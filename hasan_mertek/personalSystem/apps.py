from django.apps import AppConfig


class PersonalsystemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "personalSystem"

    def ready(self):
        import personalSystem.signals
