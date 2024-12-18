# Generated by Django 4.2.13 on 2024-09-12 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailimages", "0026_delete_uploadedimage"),
        ("essays", "0020_alter_essaypage_intro"),
    ]

    operations = [
        migrations.AddField(
            model_name="essaypage",
            name="preview_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.image",
            ),
        ),
    ]
