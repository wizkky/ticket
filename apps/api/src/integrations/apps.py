from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IntegrationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "integrations"
    verbose_name = _("Integrations")

    def ready(self) -> None:
        """Populate the provider registry, install the per-app exception handlers, and wire up signals."""
        from integrations import signals  # noqa: F401
        from integrations.exception_handlers import register as register_exception_handlers
        from integrations.registry import populate

        populate()
        register_exception_handlers()
