from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("taggit/", include("taggit_selectize.urls")),
    path("about/", views.about, name="about"),
    path("manuscript/", views.DocumentListView.as_view(), name="manuscript"),
]
