from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import Document


def get_page_range_sort_key(document):
    # Custom function to extract the numeric values from page_range
    try:
        # Split the page_range into components (e.g., "4-5" becomes ["4", "5"])
        components = document.page_range.split("-")
        # Convert each component to an integer
        return [int(component) for component in components]
    except (ValueError, AttributeError):
        # Handle cases where the conversion fails or page_range is None
        return []


def index(request: HttpRequest):
    return render(request, "index.html", {})


def about(request: HttpRequest):
    return render(request, "about.html", {})


def manuscript(request: HttpRequest):
    documents = Document.objects.all()
    sorted_documents = sorted(documents, key=get_page_range_sort_key)
    return render(request, "manuscript.html", {"documents": sorted_documents})


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
        return Document.objects.all().order_by("document_id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["document_list"] = Document.objects.all().order_by("document_id")
        return context

    def get_absolute_url(self):
        """Return the URL for this document."""
        return reverse("document", args=[str(self.id)])


class DocumentDetailView(generic.DetailView):
    model = Document
    context_object_name = "manuscript_page"
    template_name = "manuscript_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fragments"] = self.object.fragment_set.order_by("line_number")
        return context
