from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from prose.models import Document
from taggit_selectize.managers import TaggableManager


class Author(models.Model):
    full_name = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="How the author's name should be displayed, if different from their full name.",
    )
    bio = models.TextField(
        max_length=600,
        blank=True,
        help_text="A short biography of the author. Max characters is 600.",
    )
    email = models.EmailField(help_text="The author's email address.")

    def __str__(self):
        return self.full_name


class Essay(models.Model):
    class Meta:
        ordering = ["-published_date"]

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        default="",
        editable=False,
    )
    body = models.OneToOneField(Document, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(
        default=False, help_text="Publish this essay? If checked, yes."
    )

    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if no slug is provided, use the title to create one
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        # if no published date is provided, use the current date
        if not self.published_date and self.published:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)
