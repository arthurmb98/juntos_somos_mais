from django.apps import AppConfig

class UserDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_data'

    def ready(self):
        import user_data.signals  # Importa sinais para garantir que sejam registrados
