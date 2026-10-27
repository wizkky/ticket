from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QuestionnairesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "questionnaires"
    verbose_name = _("Questionnaires")

    def ready(self) -> None:
        """Register the per-app exception handlers."""
        from questionnaires.exception_handlers import register as register_exception_handlers

        register_exception_handlers()
