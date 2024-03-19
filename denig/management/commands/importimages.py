import logging
import os
import re

from dateutil.parser import parse
from django.core.files import File
from django.core.management.base import BaseCommand

from denig.models import Document, Image

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Associate manually-added images from the static/upload/ directory to the data objects."

    def add_arguments(self, parser):
        parser.add_argument(
            "--filepath",
            type=str,
            help="The path to the local images. Defaults to `static/upload/`.",
            default="static/upload",
        )

    def handle(self, *args, **options):
        filepath = options["filepath"]
        for filename in os.listdir(filepath):
            document_id, _ = os.path.splitext(filename)
            try:
                document = Document.objects.get(document_id=document_id)
                with open(os.path.join(filepath, filename), "rb") as f:
                    image = Image(
                        related_document=document,
                        image=File(f, name=filename),
                    )
                    image.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully associated {filename}.")
                    )
            except Document.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Document {document_id} does not exist.")
                )
