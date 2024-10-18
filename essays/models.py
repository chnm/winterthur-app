from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from prose.models import Document
from taggit_selectize.managers import TaggableManager
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Orderable, Page
from wagtail.search import index

from denig.models import Document


class OrderedDocumentChooserPanel(PageChooserPanel):
    def get_form_class(self):
        form_class = super().get_form_class()
        form_class.base_fields[self.field_name].queryset = Document.objects.order_by(
            "document_id"
        )
        return form_class


class GalleryImage(Orderable):
    page = ParentalKey("ForensicPage", related_name="gallery_images")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]


class ForensicPage(Page):
    body = RichTextField(blank=True)
    preview_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="If no preview image is provided, the first image in the gallery will be used.",
    )
    link_to_manuscript_page = models.URLField(blank=True)
    related_manuscript_page = models.ForeignKey(
        Document, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("preview_image"),
        OrderedDocumentChooserPanel("related_manuscript_page"),
        InlinePanel("gallery_images", label="Gallery images"),
    ]


class EssayIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]


class EssayPage(Page):
    date = models.DateField("Post date")
    author = models.CharField(max_length=250)
    intro = models.CharField(max_length=250, blank=True, null=True)
    body = RichTextField(
        blank=True,
        features=[
            "h2",
            "h3",
            "h4",
            "bold",
            "italic",
            "ol",
            "ul",
            "link",
            "document-link",
            "blockquote",
            "image",
            "embed",
            "hr",
        ],
    )
    author_bio = RichTextField(blank=True)
    preview_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    doi = RichTextField(blank=True)
    doi_url = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("author"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("author"),
        FieldPanel("author_bio"),
        FieldPanel("preview_image"),
        FieldPanel("doi"),
        FieldPanel("doi_url"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]


class EssayPageGalleryImage(Orderable):
    page = ParentalKey(
        EssayPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]
