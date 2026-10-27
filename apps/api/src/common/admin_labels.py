"""Translation of human-readable administrative metadata."""

import typing as t

from django.utils.text import capfirst
from django.utils.translation import gettext as _


def admin_label(value: t.Any) -> str:
    """Translate a label without importing admin classes or changing model metadata."""
    text = str(value) if value is not None else ""
    return _(capfirst(text))
