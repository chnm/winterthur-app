# Generated by Django 4.2.13 on 2024-06-12 16:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("denig", "0034_alter_document_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="slug",
            field=models.SlugField(default=None, null=True, unique=True),
        ),
    ]