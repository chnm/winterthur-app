import logging

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from openpyxl import load_workbook

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
        fragment_df = pd.read_excel(file_path, sheet_name=sheet_name)
        for index, row in fragment_df.iterrows():
            try:
                document = Document.objects.get(document_id=row["item_file_name"])
            except Document.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f"Document {row['item_file_name']} does not exist."
                    )
                )
                continue

            fragment = Fragment.objects.create(
                document=document,
                line_number=row["line_number"],
                transcription=row["transcription"],
                notes=row["notes"],
            )
            languages = Language.objects.filter(
                display_name__in=row["languages"].split(",")
            )
            fragment.languages.set(languages)
