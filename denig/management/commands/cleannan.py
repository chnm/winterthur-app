from django.core.management.base import BaseCommand
from django.db.models import Q

from denig.models import Document, Fragment


class Command(BaseCommand):
    help = "Clean up nan values from the database."

    def handle(self, *args, **kwargs):
        fields_to_clean = ["transcription", "notes"]

        for field in fields_to_clean:
            nan_filter = Q(**{f"{field}__iexact": "nan"})
            records = Fragment.objects.filter(nan_filter)

            for record in records:
                setattr(record, field, "")
                record.save()
