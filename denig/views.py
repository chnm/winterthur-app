from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

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


def scholarship(request: HttpRequest):
    return render(request, "scholarship.html", {})


"""def forensics(request: HttpRequest):
    return render(request, "forensics.html", {})"""


def music(request: HttpRequest):
    return render(request, "music.html", {})


def education(request: HttpRequest):
    return render(request, "education.html", {})


class DocumentListView(generic.ListView):
    paginate_by = (
        # to get the first page layout to work, we need to offset by an odd number
        11
    )
    model = Document
    context_object_name = "document_list"
    template_name = "manuscript.html"

    def get_queryset(self):
        # This method ensures the documents are ordered by 'document_id'
        return Document.objects.all().order_by("document_id")

    def get_absolute_url(self):
        """Return the URL for this document."""
        return reverse("document", args=[str(self.id)])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context.get("page_obj")
        context["is_first_page"] = page_obj and page_obj.number == 1
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
        try:
            current_document = self.get_queryset().get(slug=self.kwargs["slug"])
        except Document.DoesNotExist:
            current_document = None

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
            print(
                f"Next image URL: {next_image_url}, Cleaned next image URL: {cleaned_next_image_url}"
            )
        else:
            cleaned_next_image_url = None

        context["previous_page"] = previous_page
        context["next_page"] = next_page
        context["next_page_id"] = next_page_id
        context["current_page"] = current_page
        context["page_number"] = page_number
        context["cleaned_url"] = cleaned_url
        context["next_image_url"] = cleaned_next_image_url
        context["all_pages"] = Document.objects.all().order_by("document_id")
        context["fragments"] = self.object.fragment_set.order_by("line_number")

        return context


class ForensicsListView(generic.View):
    def get(self, request, *args, **kwargs):
        image_list = Image.objects.filter(image_type="forensics").order_by("id")
        document_list = (
            Document.objects.filter(attached_images__image_type="forensics")
            .order_by("id")
            .distinct()
        )
        return render(
            request,
            "forensics.html",
            {"image_list": image_list, "document_list": document_list},
        )


'''class ForensicsListView(generic.ListView):
    model = Image
    context_object_name = "image_list"
    template_name = "forensics.html"

    def get_queryset(self):
        return Image.objects.all().order_by("related_document_id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #forensic_images = Image.objects.filter(image_type = "recto")
        #document_list = Document.objects.all().order_by("document_id")
        image_list = Image.objects.filter(image_type = 'forensics').order_by("related_document_id")
        context["image_list"] = image_list

        return context

    def get_absolute_url(self):
        """Return the URL for this document."""
        return reverse("document", args=[str(self.id)])'''


class ForensicDetailView(generic.DetailView):
    model = Image
    context_object_name = "forensic_page"
    template_name = "forensic_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current image
        current_image = self.object

        # Get previous and next pages
        try:
            previous_page = (
                Image.objects.filter(id__lt=current_image.id).order_by("-id").first()
            )
        except Image.DoesNotExist:
            previous_page = None

        try:
            next_page = (
                Image.objects.filter(id__gt=current_image.id).order_by("id").first()
            )
        except Image.DoesNotExist:
            next_page = None

        # Get current page
        try:
            current_page = Document.objects.get(
                document_id=current_image.related_document
            )
        except Document.DoesNotExist:
            current_page = None

        # Get the page number of the current document
        try:
            page_number = current_image.related_document.page_range.split("-")[0]
        except AttributeError:
            page_number = None

        context["previous_image"] = previous_page
        context["next_image"] = next_page
        context["current_image"] = current_page
        context["page_number"] = page_number
        context["all_pages"] = Image.objects.filter(image_type="forensics").order_by(
            "id"
        )
        context["documents"] = (
            Document.objects.filter(attached_images__image_type="forensics")
            .order_by("id")
            .distinct()
        )
        # context["fragments"] = self.object.fragment_set.order_by("line_number")

        return context
