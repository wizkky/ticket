from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PollsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "polls"
    verbose_name = _("Polls")

    def ready(self) -> None:
        """Import signal receivers and register the per-app exception handlers."""
        import polls.signals  # noqa: F401  (registers receivers)
        from polls.exception_handlers import register as register_exception_handlers

        register_exception_handlers()
