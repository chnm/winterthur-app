# Generated by Django 4.2.13 on 2024-08-21 16:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("essays", "0019_essaypage_doi_essaypage_doi_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="essaypage",
            name="intro",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]