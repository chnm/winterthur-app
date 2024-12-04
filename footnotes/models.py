from django.db import models
from django.db.models.functions import NullIf
from multiselectfield import MultiSelectField


class Footnote(models.Model):
    """a footnote that links from a denig.models.Document to a class:Fragment"""

    source = models.ForeignKey(
        "denig.Fragment",
        on_delete=models.CASCADE,
        help_text="Select a fragment that is associated with this footnote.",
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Location of the footnote in the source document (e.g., page number or page range).",
    )

    FOOTNOTE_TYPE = (
        ("O", "Original"),
        ("A", "Annotation"),
    )

    footnote_type = models.CharField(
        choices=FOOTNOTE_TYPE,
        blank=True,
        null=True,
        max_length=1,
        help_text="Footnote type",
    )
    content = models.TextField(
        blank=True,
        null=True,
    )
    notes = models.TextField(
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "source",
            # sort footnote with empty locations after footnote with location
            # (sort digital editions after other footnotes for same source)
            NullIf("location", models.Value("")).asc(nulls_last=True),
        ]
        constraints = [
            # only allow one digital edition per source for a document
            models.UniqueConstraint(
                fields=("source", "footnote_type"),
                name="one_fragment_per_page",
                condition=models.Q(footnote_type__contains="O"),  # X = DIGITAL_EDITION
            )
        ]

    def __str__(self):
        return f"{self.source} {self.location}"
