from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.core.exceptions import ValidationError
from django.db import models
from django.forms.widgets import HiddenInput, Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from footnotes.models import Footnote

from .models import Collection, Document, Fragment, Language, MusicScore

admin.site.register(Collection)
admin.site.register(Language)
admin.site.register(MusicScore)

"""
Setup export resource classes
"""


class DocumentResource(resources.ModelResource):
    class Meta:
        model = Document


class FragmentResource(resources.ModelResource):
    document = fields.Field(
        column_name="document",
        attribute="document",
        widget=ForeignKeyWidget(Document, "id"),
    )

    class Meta:
        model = Fragment


"""
Overrides for admin widgets
"""


class CustomAdminFileWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        result = []
        if hasattr(value, "url"):
            result.append(
                f"""<a href="{value.url}" target="_blank">
                      <img 
                        src="{value.url}" alt="{value}" 
                        width="700" height="auto"
                        style="object-fit: cover;"
                      />
                    </a>"""
            )
        result.append(super().render(name, value, attrs, renderer))
        return format_html("".join(result))


"""
Setup admin classes
"""


class FragmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("__str__", "line_number", "document", "last_modified")
    list_filter = ("document", "languages")
    search_fields = ("transcription", "notes")

    resource_classes = [FragmentResource]


admin.site.register(Fragment, FragmentAdmin)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = ()
        widgets = {
            "language_note": Textarea(attrs={"rows": 1}),
            "needs_review": Textarea(attrs={"rows": 3}),
            "notes": Textarea(attrs={"rows": 3}),
            "image_order_override": HiddenInput(),
        }


class DocumentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = DocumentForm
    list_display = (
        "docside",
        "page_range",
        "notes",
        "doctype",
        "all_tags",
        "last_modified",
    )
    readonly_fields = (
        "created",
        "last_modified",
        # "admin_thumbnails",
        "id",
    )
    search_fields = (
        "fragments",
        "tags__name",
        "description",
        "notes",
        "id",
    )
    list_filter = (
        "docside",
        "doctype",
        "tags",
    )

    formfield_overrides = {models.FileField: {"widget": CustomAdminFileWidget}}
    resource_classes = [DocumentResource]


class FragmentInline(admin.TabularInline):
    model = Fragment
    extra = 0
    verbose_name = "Fragment"
    verbose_name_plural = "Fragments"
    fields = (
        "line_number",
        "transcription",
        "languages",
        "notes",
    )
    # readonly_fields = ("admin_thumbnails",)
    formfield_overrides = {
        models.ManyToManyField: {"widget": forms.CheckboxSelectMultiple},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("line_number")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "document":
            kwargs["initial"] = request.resolver_match.kwargs["object_id"]
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def admin_thumbnails(self, obj):
    #     return format_html("<img src='{}' />", obj.image.url)

    # admin_thumbnails.short_description = "Image"


DocumentAdmin.inlines = [FragmentInline]


admin.site.register(Document, DocumentAdmin)


class FootnoteInline(admin.TabularInline):
    """Add footnotes within the Fragment form."""

    model = Footnote
    extra = 0
    verbose_name = "Footnote"
    verbose_name_plural = "Footnotes"
    fields = ("content", "source", "id")
    readonly_fields = ("source", "id")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("id")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "document":
            kwargs["initial"] = request.resolver_match.kwargs["object_id"]
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def footnote(self, obj):
        return format_html("<a href='{}'>{}</a>", obj.get_absolute_url(), obj)

    footnote.short_description = "Footnote"


FragmentAdmin.inlines = [FootnoteInline]
