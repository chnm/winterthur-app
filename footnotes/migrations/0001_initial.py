# Generated by Django 4.1.7 on 2023-03-30 18:38

import django.db.models.deletion
import django.db.models.functions.comparison
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("denig", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Footnote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True,
                        help_text="Location of the footnote in the source document (e.g., page number or page range).",
                        max_length=255,
                    ),
                ),
                (
                    "footnote_type",
                    models.CharField(
                        blank=True,
                        choices=[("O", "Original"), ("A", "Annotation")],
                        help_text="Footnote type",
                        max_length=1,
                        null=True,
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                ("content", models.JSONField(blank=True, null=True)),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="denig.document"
                    ),
                ),
            ],
            options={
                "ordering": [
                    "source",
                    models.OrderBy(
                        django.db.models.functions.comparison.NullIf(
                            "location_sort", models.Value("")
                        ),
                        nulls_last=True,
                    ),
                ],
            },
        ),
        migrations.AddConstraint(
            model_name="footnote",
            constraint=models.UniqueConstraint(
                condition=models.Q(("footnote_type__contains", "O")),
                fields=("source", "footnote_type"),
                name="one_fragment_per_page",
            ),
        ),
    ]
