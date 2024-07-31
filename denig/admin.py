from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.core.exceptions import ValidationError
from django.db import models
from django.forms.widgets import HiddenInput, Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from denig.resources import DocumentResource, FragmentResource
from footnotes.models import Footnote

from .models import Collection, Document, Fragment, Image, Language, MusicScore


# Overrides for admin widgets
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


# Setup admin classes
class FragmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("__str__", "line_number", "link_to_document", "last_modified")
    list_filter = ("document", "languages")
    search_fields = ("transcription", "notes")

    resource_classes = [FragmentResource]

    def link_to_document(self, obj):
        url = reverse("admin:denig_document_change", args=[obj.document.id])
        return format_html('<a href="{}">{}</a>', url, obj.document)

    link_to_document.short_description = "Document"


class ImagesInline(admin.StackedInline):
    model = Image
    extra = 0
    readonly_fields = ("image_preview",)
    classes = ("collapse",)


class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image_thumbnail")

    list_per_page = 10

    def image_thumbnail(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url)

    image_thumbnail.short_description = "Image Thumbnail"

    # def url_to_object(self, obj):
    #     url = reverse("admin:documents_object_change", args=[obj.related_document.id])
    #     return format_html('<a href="{}">{}</a>', url, obj.related_document.item_id)

    # url_to_object.short_description = "View the page associated with this image"


class MusicScoreInline(admin.StackedInline):
    model = MusicScore
    extra = 0
    classes = ("collapse",)


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


@admin.action(description="Mark as Music Score")
def mark_as_music_score(modeladmin, request, queryset):
    queryset.update(doctype="music score")


class DocumentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = DocumentForm
    list_display = (
        "document_id",
        "docside",
        "page_range",
        "doctype",
        "all_tags",
        "last_modified",
    )
    readonly_fields = (
        "created",
        "last_modified",
        "id",
    )
    search_fields = (
        "fragment__transcription",
        "description",
        "notes",
    )
    list_filter = (
        "docside",
        "doctype",
        "tags",
    )
    actions = [mark_as_music_score]

    formfield_overrides = {models.FileField: {"widget": CustomAdminFileWidget}}
    resource_classes = [DocumentResource]

    # prepopulated_fields = {"slug": ("page_range",)}


class FootnoteInline(admin.TabularInline):
    """Add footnotes within the Fragment form."""

    model = Footnote
    extra = 0
    classes = ("collapse",)
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
    footnote.long_description = "Footnotes"


class FragmentInline(admin.StackedInline):
    model = Fragment
    extra = 0
    classes = ("collapse",)
    verbose_name = "Fragment"
    verbose_name_plural = "Fragments"
    fields = (
        "line_number",
        "transcription",
        "languages",
        "notes",
    )
    formfield_overrides = {
        models.ManyToManyField: {"widget": forms.CheckboxSelectMultiple},
    }
    inlines = [FootnoteInline]
    show_change_link = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("line_number")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "document":
            kwargs["initial"] = request.resolver_match.kwargs["object_id"]
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


DocumentAdmin.inlines = [FragmentInline, ImagesInline, MusicScoreInline]


# Register
admin.site.register(Fragment, FragmentAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Collection)
admin.site.register(Language)
admin.site.register(MusicScore)
admin.site.register(Image, ImageAdmin)
