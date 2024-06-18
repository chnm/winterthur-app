from django.core.management.base import BaseCommand

from denig.models import Document


class Command(BaseCommand):
    help = "Split concatenated tags into separate tags"

    def handle(self, *args, **kwargs):
        objects = Document.objects.all()

        for obj in objects:
            tags = obj.tags.names()
            updated = False

            for tag in tags:
                if " ; " in tag:
                    split_tags = tag.split(" ; ")
                    obj.tags.remove(tag)

                    for split_tag in split_tags:
                        obj.tags.add(split_tag.strip())

                    updated = True

            if updated:
                obj.save()

        self.stdout.write(self.style.SUCCESS("Successfully split concatenated tags"))
