from django.contrib import admin
from django.urls import include, path

from essays.models import Author, Essay

admin.site.register(Author)
admin.site.register(Essay)
