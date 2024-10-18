from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views import generic
from wagtail.models import Page

from .models import Document, Image


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


class DocumentListView(generic.ListView):
    model = Document
    context_object_name = "document_list"
    template_name = "manuscript.html"
    paginate_by = 12

    def paginate_queryset(self, queryset, page_size):
        """
        Custom paginate queryset to handle the offset on page 2.
        """
        paginator = super().get_paginator(queryset, page_size)
        page = self.request.GET.get("page")
        if page is None or page == "1":
            # For the first page, we want 13 items (cover + 12 manuscript pages)
            page_obj = paginator.page(1)
            page_obj.object_list = queryset[:13]
        else:
            # For subsequent pages, ensure no overlap
            page_number = paginator.validate_number(page)
            start_index = 13 + (page_number - 2) * page_size
            end_index = start_index + page_size
            page_obj = paginator.page(page_number)
            page_obj.object_list = queryset[start_index:end_index]
        return (paginator, page_obj, page_obj.object_list, page_obj.has_other_pages())

    def get_queryset(self):
        # Ensures the documents are ordered by 'document_id'
        return Document.objects.all().order_by("document_id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context.get("page_obj")
        context["is_first_page"] = page_obj and page_obj.number == 1
        context["all_pages"] = Document.objects.all().order_by("document_id")

        return context


class DocumentDetailView(generic.DetailView):
    model = Document
    context_object_name = "manuscript_page"

    def get_template_names(self):
        if self.object.doctype == "music score":
            return ["manuscript_musicscore.html"]
        else:
            return ["manuscript_page.html"]

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
        current_document = get_object_or_404(Document, slug=self.kwargs["slug"])

        # Get previous and next pages
        try:
            previous_page = (
                Document.objects.filter(document_id__lt=current_document.document_id)
                .order_by("-document_id")
                .first()
            )
        except Document.DoesNotExist:
            previous_page = None

        # get the next page slug
        try:
            next_page = (
                Document.objects.filter(document_id__gt=current_document.document_id)
                .order_by("document_id")
                .first()
            )
        except Document.DoesNotExist:
            next_page = None

        # Calculate the id of the next page for music scores
        if current_document.doctype == "music score" and next_page:
            next_page_id = next_page.id + 1
        else:
            next_page_id = next_page.id if next_page else None

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

        # Get the image URL and clean it (for using object store)
        if current_document.attached_images.all().exists():
            first_image_url = current_document.attached_images.all()[0].image.url
            cleaned_url = self.clean_url(first_image_url)
        else:
            cleaned_url = None

        if next_page.attached_images.all().exists():
            next_image_url = next_page.attached_images.all()[0].image.url
            cleaned_next_image_url = self.clean_url(next_image_url)
        else:
            cleaned_next_image_url = None

        # Provide the forensic images if available
        if current_document.attached_images.filter(image_type="forensics").exists():
            forensic_images = current_document.attached_images.filter(
                image_type="forensics"
            )
        else:
            forensic_images = None

        context.update(
            {
                "previous_page": previous_page,
                "next_page": next_page,
                "next_page_id": next_page_id,
                "current_page": current_page,
                "page_number": page_number,
                "cleaned_url": cleaned_url,
                "next_image_url": cleaned_next_image_url,
                "all_pages": Document.objects.all().order_by("document_id"),
                "fragments": self.object.fragment_set.order_by("line_number"),
                "forensic_images": forensic_images,
            }
        )

        return context


class MusicListView(generic.View):
    def get(self, request, *args, **kwargs):
        hymnal_list = (
            Document.objects.filter(doctype="music score")
            .order_by("document_id")
            .distinct()
        )
        return render(
            request,
            "music.html",
            {"hymnal_list": hymnal_list},
        )
