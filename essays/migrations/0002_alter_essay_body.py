# Generated by Django 4.1.7 on 2023-06-23 14:09

import prose.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("essays", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="essay",
            name="body",
            field=prose.fields.RichTextField(),
        ),
    ]
