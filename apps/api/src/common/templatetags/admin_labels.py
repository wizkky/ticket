"""Translate admin metadata at the presentation layer only."""

import typing as t

from django import template

from common.admin_labels import admin_label

register = template.Library()


@register.filter
def caudal_label(value: t.Any) -> str:
    """Look up headings and labels without translating user-authored record values."""
    return admin_label(value)
