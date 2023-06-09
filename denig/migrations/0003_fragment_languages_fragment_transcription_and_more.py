# Generated by Django 4.1.7 on 2023-03-30 19:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("denig", "0002_alter_document_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="fragment",
            name="languages",
            field=models.ManyToManyField(
                blank=True,
                help_text="Language(s) of the fragment.",
                to="denig.language",
            ),
        ),
        migrations.AddField(
            model_name="fragment",
            name="transcription",
            field=models.TextField(
                blank=True, help_text="Transcription of the fragment."
            ),
        ),
        migrations.AlterField(
            model_name="collection",
            name="library",
            field=models.CharField(
                blank=True, default="Winterthur Museum, Garden & Library", max_length=55
            ),
        ),
        migrations.AlterField(
            model_name="fragment",
            name="notes",
            field=models.TextField(
                blank=True,
                help_text="Notes about the fragment. These will not be public.",
            ),
        ),
    ]
