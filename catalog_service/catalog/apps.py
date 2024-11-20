from django.apps import AppConfig
from django.core.management import call_command

class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"
    
    def ready(self):
        try:
            call_command('loaddata', 'books')
        except Exception as e:
            print(f"Error loading fixtures: {e}")