# Generated by Django 4.2.13 on 2024-06-12 15:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("denig", "0032_document_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="slug",
            field=models.SlugField(null=True, unique=True),
        ),
    ]
