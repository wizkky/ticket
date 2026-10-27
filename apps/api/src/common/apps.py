from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommonConfig(AppConfig):
    """Configuration for the common app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "common"
    verbose_name = _("Common")

    def ready(self) -> None:
        """Initialize app-level services.

        Called once Django is fully loaded.
        """
        # Import and initialize observability
        from common.observability import init_profiling, init_tracing

        init_tracing()
        init_profiling()

        # Importing the module runs its @register() decorators.
        import common.checks  # noqa: F401
