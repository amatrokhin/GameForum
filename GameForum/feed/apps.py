from django.apps import AppConfig


class FeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feed'

    # override ready method to import all handler functions from signals
    def ready(self):
        import feed.signals
