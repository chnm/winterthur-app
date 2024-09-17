import logging
from functools import cached_property

from django.conf import settings
from django.db import models
from django.db.models.functions.text import Lower
from django.dispatch import receiver
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django_extensions.db.fields import AutoSlugField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from import_export.admin import ImportExportMixin
from taggit_selectize.managers import TaggableManager

from footnotes.models import Footnote

logger = logging.getLogger(__name__)


class CollectionManager(models.Manager):
    """Manager for Collection model."""

    def get_by_natural_key(self, library):
        return self.get(library=library)


class Collection(models.Model):
    """Collection or library that holds an archival item."""

    library = models.CharField(
        max_length=55, blank=True, default="Winterthur Museum, Garden & Library"
    )
    location = models.CharField(
        max_length=255, help_text="Location of the library.", default="Winterthur, DE"
    )

    objects = CollectionManager()

    def __str__(self):
        return self.library

    def natural_key(self):
        """natural key"""
        return self.library


class LanguageManager(models.Model):
    """Manager for Language model."""

    def get_by_natural_key(self, language):
        """natural key"""
        return self.get(language=language)


class Language(models.Model):
    """Language of a page item."""

    language = models.CharField(max_length=55, blank=True)
    display_name = models.CharField(
        max_length=255,
        blank=True,
        unique=True,
        null=True,
    )
    iso_code = models.CharField(
        "ISO Code",
        max_length=3,
        blank=True,
        help_text="ISO 639 code for this language (2 or 3 letters)",
    )

    objects = LanguageManager()

    def __str__(self):
        return self.language

    def natural_key(self):
        """natural key"""
        return self.language

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        ordering = ["language"]
        constraints = [
            models.UniqueConstraint(
                fields=["language", "display_name"], name="unique_language_display_name"
            )
        ]


class FragmentManager(models.Manager):
    def get_by_natural_key(self, collection):
        return self.get(collection=collection)


class Fragment(ImportExportMixin, models.Model):
    """A single fragment of the text."""

    id = models.AutoField(primary_key=True)
    line_number = models.IntegerField(
        blank=True, null=True, help_text="Line number of the fragment."
    )
    document = models.ForeignKey(
        "Document",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="Link to a document for this fragment.",
    )
    transcription = models.TextField(
        blank=True, help_text="Transcription of the fragment."
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Internal notes",
        help_text="Notes about the fragment. These will not be public.",
    )
    languages = models.ManyToManyField(
        Language,
        blank=True,
        help_text="Select the language of this fragment.",
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = FragmentManager()

    class Meta:
        ordering = ["document", "created"]

    def __str__(self):
        return (
            "Fragment line "
            + str(self.line_number)
            + " - "
            + str(self.languages.first().language if self.languages.first() else "")
            + " translation"
        )

    @staticmethod
    def admin_thumbnails(images, labels, canvases=[], selected=[]):
        return mark_safe(
            " ".join(
                '<img src="%s" loading="lazy" height="200" title="%s" %s%s>'
                % (
                    image,
                    labels[i],
                    f'data-canvas="{list(canvases)[i]}" ' if canvases else "",
                    'class="selected" /' if i in selected else "/",
                )
                for i, image in enumerate(images)
            )
        )

    @property
    def attribution(self):
        """Generate an attribution for this fragment."""
        return self.collection.library


class DocumentTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(document_type=name)


class DocumentType(models.Model):
    """A document indicates an individual page (verso/recto) or a page spread
    (verso and recto)."""

    name = models.CharField(max_length=255, unique=True)
    display_labels = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional label to display on the public site.",
    )
    objects = DocumentTypeManager()

    def __str__(self):
        current_language = get_language()
        return current_language or self.display_labels or self.name

    def natural_key(self):
        return (self.name,)

    @cached_property
    def object_by_label(self, cls):
        return {
            (docside.display_labels or docside.name): docside
            for docside in cls.objects.all()
        }


class Image(models.Model):
    IMAGE_TYPES = (
        ("recto", "Recto"),
        ("verso", "Verso"),
        ("verso and recto", "Verso and Recto"),
        ("music score", "Music Score"),
        ("forensics", "Forensics"),
    )
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="images/")
    related_document = models.ForeignKey(
        "Document",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="attached_images",
    )
    image_type = models.CharField(
        max_length=255,
        blank=True,
        choices=IMAGE_TYPES,
        default="recto",
    )
    thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(400, 350)],
        format="JPEG",
        options={"quality": 90},
    )
    caption = models.TextField(
        blank=True,
        null=True,
        help_text="Caption for the image.",
    )

    def __str__(self):
        return f"{self.related_document} - {self.image}"

    def image_preview(self):
        if self.image:
            return mark_safe(
                '<img src="%s" style="width:100px; height:100px;" />'
                % self.thumbnail.url
            )
        else:
            return "No image attached"


class Document(ImportExportMixin, models.Model):
    RECTO = "recto"
    VERSO = "verso"
    RECTO_VERSO = "verso and recto"

    SIDE_CHOICES = (
        (RECTO, "Recto"),
        (VERSO, "Verso"),
        (RECTO_VERSO, "Verso and Recto"),
    )

    DOCTYPE_CHOICES = (
        ("music score", "Music Score"),
        ("illumination", "Illumination"),
        ("text", "Text"),
    )

    id = models.AutoField(editable=False, primary_key=True)
    document_id = models.CharField(max_length=255, unique=True, blank=False, null=True)
    description = models.TextField(blank=True, null=True)
    docside = models.CharField(
        max_length=255,
        blank=True,
        choices=SIDE_CHOICES,
        default=RECTO,
        verbose_name="Document side",
    )
    doctype = models.CharField(
        max_length=255,
        blank=True,
        choices=DOCTYPE_CHOICES,
        default="text",
        verbose_name="Document type",
    )
    page_range = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Page",
        help_text="Page or page range of the document.",
    )
    tags = TaggableManager(blank=True, related_name="document_tags")
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Internal notes",
        help_text="Internal notes about the item. These are not public.",
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = FragmentManager()

    PLACEHOLDER_CANVAS = {
        "image": {
            "info": static("files/image-unavailable.png"),
        },
        "placeholder": True,
    }

    slug = AutoSlugField(
        null=True, default=None, unique=True, editable=True, populate_from="page_range"
    )

    class Meta:
        pass

    def __str__(self):
        return "Page" + " " + str(self.page_range) + " " + str(self.docside)

    def save(self, *args, **kwargs):
        """Save the document."""
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            raise e

    def all_languages(self):
        """Return all languages of the document."""
        return ", ".join([str(language) for language in self.languages.all()])

    all_languages.short_description = "language"

    def all_tags(self):
        return ", ".join(t.name for t in self.tags.all())

    all_tags.short_description = "tags"

    def alphabetize_tags(self):
        return self.tags.order_by(Lower("name"))

    def get_absolute_url(self):
        """Return the URL for this document."""
        """changed from return reverse("document", args=[str(self.id)]) """
        return reverse("document", kwargs={"slug": self.slug})

    @property
    def permalink(self):
        lang = get_language() or settings.LANGUAGE_CODE
        return self.get_absolute_url().replace(f"/{lang}/", "/")

    @property
    def title(self):
        return self.description

    @property
    def file_url(self):
        if self.item_file and hasattr(self.item_file, "url"):
            return self.item_file.url


class MusicScore(ImportExportMixin, models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    page_range = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Page",
        help_text="Page or page range of the document.",
    )
    composer = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Composer of the music, if known.",
    )
    arrangement_by = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Name of who arranged the music score.",
    )
    translated_by = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Name of who translated the music score.",
    )
    related_document = models.ForeignKey(
        Document,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="music_scores",
    )
    sheet_music = models.FileField(
        upload_to="media/",
        blank=True,
        null=True,
        help_text="Upload a file (PDF or PNG).",
        verbose_name="Sheet music",
    )
    audio_recording_file = models.FileField(
        upload_to="media/",
        blank=True,
        null=True,
        help_text="Upload a file.",
        verbose_name="Audio recording",
    )

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.composer} - {self.title}"
