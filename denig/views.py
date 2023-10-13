from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import Document


def index(request: HttpRequest):
    return render(request, "index.html", {})


def about(request: HttpRequest):
    return render(request, "about.html", {})


def manuscript(request: HttpRequest):
    return render(request, "manuscript.html", {})


def scholarship(request: HttpRequest):
    return render(request, "scholarship.html", {})


def forensics(request: HttpRequest):
    return render(request, "forensics.html", {})


def music(request: HttpRequest):
    return render(request, "music.html", {})


def education(request: HttpRequest):
    return render(request, "education.html", {})


class DocumentListView(generic.ListView):
    model = Document
    context_object_name = "document_list"
    template_name = "manuscript.html"

    def get_queryset(self):
        return Document.objects.all().order_by("-page_range")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["document_list"] = Document.objects.all().order_by("-page_range")
        return context

    def get_absolute_url(self):
        """Return the URL for this document."""
        return reverse("document", args=[str(self.id)])


class DocumentDetailView(generic.DetailView):
    model = Document
    context_object_name = "manuscript_page"
    template_name = "manuscript_page.html"
