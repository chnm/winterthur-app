from django.db import models
from taggit_selectize.managers import TaggableManager


class Author(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    bio = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return self.user.get_username()


class Essay(models.Model):
    class Meta:
        ordering = ["-published_date"]

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    body = models.TextField()
    meta_description = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    tags = TaggableManager()
