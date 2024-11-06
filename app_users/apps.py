from django.apps import AppConfig


class AppUsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_users"

    def ready(self) -> None:
        import app_users.signals

        super().ready()
