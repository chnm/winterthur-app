# Generated by Django 4.1.7 on 2023-03-30 19:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("denig", "0007_alter_document_doctype"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="doctype",
            field=models.CharField(
                blank=True,
                choices=[
                    ("recto", "Recto"),
                    ("verso", "Verso"),
                    ("recto and verso", "Recto and Verso"),
                ],
                default="recto",
                max_length=255,
            ),
        ),
    ]