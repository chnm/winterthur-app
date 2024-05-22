from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from prose.models import Document
from taggit_selectize.managers import TaggableManager
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.search import index


class EssayIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]


class EssayPage(Page):
    date = models.DateField("Post date")
    author = models.CharField(max_length=250)
    intro = models.CharField(max_length=250)
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
