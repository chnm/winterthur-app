# Generated by Django 4.2.13 on 2024-06-13 15:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("denig", "0037_alter_document_slug"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="document",
            name="slug",
        ),
    ]
