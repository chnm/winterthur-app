# Generated by Django 4.1.7 on 2023-03-30 19:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("denig", "0011_fragment_line_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="docside",
            field=models.CharField(
                blank=True,
                choices=[
                    ("recto", "Recto"),
                    ("verso", "Verso"),
                    ("recto and verso", "Recto and Verso"),
                ],
                default="recto",
                max_length=255,
                verbose_name="Document side",
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="doctype",
            field=models.CharField(
                blank=True,
                choices=[
                    ("music score", "Music Score"),
                    ("illumination", "Illumination"),
                    ("text", "Text"),
                ],
                default="text",
                max_length=255,
            ),
        ),
    ]
