# Generated by Django 4.1.7 on 2023-10-11 19:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("essays", "0004_alter_essay_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="essay",
            name="body",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="essays.essaycontent"
            ),
        ),
    ]