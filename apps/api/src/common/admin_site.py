"""Unfold administration with localized application and model captions."""

import typing as t

from django.conf import settings
from django.contrib.admin.apps import AdminConfig
from django.http import HttpRequest
from unfold.sites import UnfoldAdminSite

from common.admin_labels import admin_label
from common.admin_modules import OPTIONAL_ADMIN_MODELS


class CaudalAdminSite(UnfoldAdminSite):
    """Translate navigation captions after Django applies its permission filters."""

    def get_app_list(self, request: HttpRequest, app_label: str | None = None) -> list[dict[str, t.Any]]:
        """Keep identifiers, URLs and permissions; localize only display names."""
        applications = super().get_app_list(request, app_label=app_label)
        if not settings.CAUDAL_SHOW_OPTIONAL_MODULES:
            for application in applications:
                application["models"] = [
                    model for model in application["models"] if model["object_name"] not in OPTIONAL_ADMIN_MODELS
                ]
            applications = [application for application in applications if application["models"]]
        for application in applications:
            application["name"] = admin_label(application["name"])
            for model in application["models"]:
                model["name"] = admin_label(model["name"])
        return t.cast(list[dict[str, t.Any]], applications)


class CaudalAdminConfig(AdminConfig):
    """Use the supported custom-site configuration of Django and Unfold."""

    default_site = "common.admin_site.CaudalAdminSite"
