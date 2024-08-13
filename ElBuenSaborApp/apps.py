from django.apps import AppConfig

class ElbuensaborappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ElBuenSaborApp'

    def ready(self):
        # Importar el archivo signals.py para registrar las señales
        import ElBuenSaborApp.signals