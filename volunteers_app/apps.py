from django.apps import AppConfig


class VolunteersAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'volunteers_app'

    def ready(self):
        import volunteers_app.signals  # noqa
