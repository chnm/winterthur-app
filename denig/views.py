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
    paginate_by = 10
    model = Document
    context_object_name = "document_list"
    template_name = "manuscript.html"

    def get_queryset(self):
        return Document.objects.all().order_by("document_id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document_list = Document.objects.all().order_by("document_id")
        context["document_list"] = document_list

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

        context["previous_page"] = previous_page
        context["next_page"] = next_page
        context["current_page"] = current_page
        context["page_number"] = page_number
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
