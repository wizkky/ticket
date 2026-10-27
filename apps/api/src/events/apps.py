from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "events"
    verbose_name = _("Events")

    def ready(self) -> None:
        """Run startup-time side effects for the events app.

        Imports the signal handlers and installs the per-app exception handlers on
        the global Ninja API. The Celery tasks live in the ``events.tasks`` package
        and are registered via Celery autodiscovery, so they need no manual import here.

        Returns:
            None: Performs registration side effects only.
        """
        from . import signals  # noqa: F401
        from .exception_handlers import register as register_exception_handlers

        register_exception_handlers()
