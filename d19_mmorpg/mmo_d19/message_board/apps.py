from django.apps import AppConfig


class MessageBoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'message_board'

    def ready(self):
        import message_board.signals
