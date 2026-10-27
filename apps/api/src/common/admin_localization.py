"""Spanish admin presentation without modifying model metadata or stored data."""

import copy
import functools
import re
import typing as t

from django import forms
from django.contrib import admin
from django.contrib.admin.filters import ChoicesFieldListFilter
from django.core.exceptions import FieldDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext as _
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import StackedInline as UnfoldStackedInline
from unfold.admin import TabularInline as UnfoldTabularInline

from common.admin_labels import admin_label


def _translate_form(form: t.Any) -> None:
    for field in form.base_fields.values():
        field.label = admin_label(field.label)
        if field.help_text:
            field.help_text = _(str(field.help_text))
        if isinstance(field, forms.ChoiceField) and not isinstance(field, forms.ModelChoiceField):
            field.choices = [
                (value, [(option, admin_label(label)) for option, label in title])
                if isinstance(title, (list, tuple))
                else (value, admin_label(title))
                for value, title in field.choices
            ]


def _translate_response(response: HttpResponse) -> HttpResponse:
    context = getattr(response, "context_data", None)
    if context and (options := context.get("opts")):
        localized_options = copy.copy(options)
        localized_options.verbose_name = admin_label(options.verbose_name)
        localized_options.verbose_name_plural = admin_label(options.verbose_name_plural)
        context["opts"] = localized_options
        if changelist := context.get("cl"):
            localized_changelist = copy.copy(changelist)
            localized_changelist.opts = localized_options
            context["cl"] = localized_changelist
        if isinstance(context.get("title"), str):
            # Django already translated the sentence; localize only the model noun.
            context["title"] = re.sub(
                rf"\b{re.escape(str(options.verbose_name))}\b",
                lambda _: localized_options.verbose_name,
                context["title"],
            )
    return response


class TranslatedChoicesFilter(ChoicesFieldListFilter):
    """Translate option captions while preserving the filter's query values."""

    def choices(self, changelist: t.Any) -> t.Iterator[dict[str, t.Any]]:
        """Return the original filter options with localized display text."""
        for option in super().choices(changelist):
            yield {**option, "display": admin_label(option["display"])}


@functools.lru_cache(maxsize=256)
def _choice_column(name: str, label: str) -> t.Callable[[t.Any], str]:
    @admin.display(description=admin_label(label), ordering=name)
    def render(obj: t.Any) -> str:
        return admin_label(getattr(obj, f"get_{name}_display")())

    render.__name__ = name
    return render


class ModelAdmin(UnfoldModelAdmin):  # type: ignore[misc]
    """Localize admin forms and headings at rendering time, preserving model contracts."""

    def get_list_display(self, request: HttpRequest) -> t.Any:
        """Localize enum captions without changing editable fields or explicit links."""
        columns = []
        for column in super().get_list_display(request):
            if (
                isinstance(column, str)
                and column not in self.list_editable
                and column not in (self.list_display_links or ())
            ):
                try:
                    field = self.model._meta.get_field(column)
                except FieldDoesNotExist:
                    field = None
                if field is not None and field.choices:
                    columns.append(_choice_column(column, str(field.verbose_name)))
                    continue
            columns.append(column)
        return columns

    def get_list_filter(self, request: HttpRequest) -> t.Any:
        """Translate enum filter choices without changing lookup names or permissions."""
        filters = []
        for option in super().get_list_filter(request):
            if isinstance(option, str) and "__" not in option:
                field = self.model._meta.get_field(option)
                if field.choices:
                    filters.append((option, TranslatedChoicesFilter))
                    continue
            filters.append(option)
        return filters

    def get_form(self, request: HttpRequest, obj: t.Any = None, change: bool = False, **kwargs: t.Any) -> t.Any:
        """Return the existing form with localized presentation labels."""
        form = super().get_form(request, obj, change=change, **kwargs)
        _translate_form(form)
        return form

    def changelist_view(self, request: HttpRequest, extra_context: t.Any = None) -> HttpResponse:
        """Keep the changelist behavior and translate its model heading."""
        return _translate_response(super().changelist_view(request, extra_context=extra_context))

    def render_change_form(
        self,
        request: HttpRequest,
        context: t.Any,
        add: bool = False,
        change: bool = False,
        form_url: str = "",
        obj: t.Any = None,
    ) -> HttpResponse:
        """Translate form headings without changing the underlying model options."""
        return _translate_response(
            super().render_change_form(
                request,
                context,
                add=add,
                change=change,
                form_url=form_url,
                obj=obj,
            )
        )


class TabularInline(UnfoldTabularInline):  # type: ignore[misc]
    """Localize inline form labels using the same catalog as the parent form."""

    def get_formset(self, request: HttpRequest, obj: t.Any = None, **kwargs: t.Any) -> t.Any:
        """Localize the inline form fields using the Spanish catalog."""
        formset = super().get_formset(request, obj, **kwargs)
        _translate_form(formset.form)
        return formset


class StackedInline(UnfoldStackedInline):  # type: ignore[misc]
    """Localize stacked forms without altering the related models."""

    def get_formset(self, request: HttpRequest, obj: t.Any = None, **kwargs: t.Any) -> t.Any:
        """Localize the inline form fields using the Spanish catalog."""
        formset = super().get_formset(request, obj, **kwargs)
        _translate_form(formset.form)
        return formset
