import logging

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from taggit.models import Tag

from denig.models import Document, Fragment, Language

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import data from a CSV file into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--filepath", type=str, help="filepath of excel file to load"
        )
        parser.add_argument("--sheetname", type=str, help="name of sheet to load")

    def handle(self, *args, **options):
        file_path = options.get("filepath", None)
        sheet_name = options.get("sheetname", None)

        try:
            with transaction.atomic():
                self.load_data(file_path, sheet_name)
                self.stdout.write(self.style.SUCCESS("Successfully loaded data."))
        except Exception as e:
            logger.exception(f"Error loading data: {str(e)}")
            self.stdout.write(
                self.style.ERROR("Error loading data. Check logs for details.")
            )

    def load_data(self, file_path, sheet_name=None):
        document_df = pd.read_excel(file_path, sheet_name="Documents")
        for index, row in document_df.iterrows():
            document = Document.objects.create(
                description=row["description"],
                document_id=row["item_image_name"],
                docside=row["document_side"],
                doctype=row["document_type"],
                page_range=row["page_range"],
                notes=row["notes"],
            )

            tags = row["tags"]
            if pd.notna(tags):
                tags = tags.split(",")
                tags = [tag.strip() for tag in tags]
            else:
                tags = []
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                document.tags.add(tag)

        # fragment_df = pd.read_excel(file_path, sheet_name="Fragments")
        # for index, row in fragment_df.iterrows():
        #     document = Document.objects.get(document_id=row["item_image_name"])
        #     fragment = Fragment.objects.create(
        #         document=document,
        #         line_number=row["line_number"],
        #         transcription=row["transcription"],
        #         notes=row["notes"],
        #     )
        #     languages = Language.objects.filter(
        #         display_name__in=row["languages"].split(",")
        #     )
        #     fragment.languages.set(languages)
