from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("forensics/", views.ForensicsListView.as_view(), name="forensics"),
    path("music/", views.MusicListView.as_view(), name="music"),
    path("education/", views.education, name="education"),
    path("scholarship/", views.scholarship, name="scholarship"),
    path("manuscript/", views.DocumentListView.as_view(), name="manuscript"),
    path(
        "manuscript/<slug:slug>/",
        views.DocumentDetailView.as_view(),
        name="manuscript_page",
    ),
    path("taggit/", include("taggit_selectize.urls")),
]
