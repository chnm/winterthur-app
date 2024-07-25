from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

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
    paginate_by = 10
    model = Document
    context_object_name = "document_list"
    template_name = "manuscript.html"

    def get_queryset(self):
        # This method ensures the documents are ordered by 'document_id'
        return Document.objects.all().order_by("document_id")

    def get_absolute_url(self):
        """Return the URL for this document."""
        return reverse("document", args=[str(self.id)])


class DocumentDetailView(generic.DetailView):
    model = Document
    context_object_name = "manuscript_page"
    template_name = "manuscript_page.html"

    def clean_url(self, url):
        # Parse the URL
        parsed_url = urlparse(url)
        # Parse the query parameters into a dictionary
        query_params = parse_qs(parsed_url.query)
        # Remove the Signature and Expiration parameters
        query_params.pop("Signature", None)
        query_params.pop("Expires", None)
        query_params.pop("AWSAccessKeyId", None)
        # Reconstruct the query string without Signature and Expiration
        new_query_string = urlencode(query_params, doseq=True)
        # Reconstruct the URL without the Signature and Expiration parameters
        cleaned_url = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                new_query_string,
                parsed_url.fragment,
            )
        )
        return cleaned_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current document
        current_document = self.object

        # Get previous and next pages
        try:
            previous_page = (
                Document.objects.filter(document_id__lt=current_document.document_id)
                .order_by("-document_id")
                .first()
            )
        except Document.DoesNotExist:
            previous_page = None

        try:
            next_page = (
                Document.objects.filter(document_id__gt=current_document.document_id)
                .order_by("document_id")
                .first()
            )
        except Document.DoesNotExist:
            next_page = None

        # Get current page
        try:
            current_page = Document.objects.get(
                document_id=current_document.document_id
            )
        except Document.DoesNotExist:
            current_page = None

        # Get the page number of the current document
        try:
            page_number = current_document.page_range.split("-")[0]
        except AttributeError:
            page_number = None

        # Get the image URL and clean it
        if current_document.attached_images.all().exists():
            first_image_url = current_document.attached_images.all()[0].image.url
            print("url", first_image_url)
            cleaned_url = self.clean_url(first_image_url)
        else:
            cleaned_url = None

        context["previous_page"] = previous_page
        context["next_page"] = next_page
        context["current_page"] = current_page
        context["page_number"] = page_number
        context["cleaned_url"] = cleaned_url
        context["all_pages"] = Document.objects.all().order_by("document_id")
        context["fragments"] = self.object.fragment_set.order_by("line_number")

        return context
