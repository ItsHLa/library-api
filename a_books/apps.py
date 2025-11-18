from django.apps import AppConfig


class ABooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_books'
    
    def ready(self) -> None:
        import a_books.signals
