# Generated by Django 4.1.7 on 2023-06-22 18:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("denig", "0015_remove_document_image_document_item_file_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="document",
            name="page",
        ),
        migrations.AddField(
            model_name="document",
            name="page_range",
            field=models.CharField(
                blank=True,
                help_text="Page or page range of the document.",
                max_length=255,
                verbose_name="Page",
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="item_file",
            field=models.FileField(
                blank=True,
                help_text="Upload a file. Click to open a larger image.",
                upload_to="files/",
                verbose_name="File preview",
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="notes",
            field=models.TextField(
                blank=True,
                help_text="Internal notes about the item. These are not public.",
            ),
        ),
    ]
